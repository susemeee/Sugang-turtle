# -*- coding: utf-8 -*-
import logging
import os
import sys
import gevent

from gevent import monkey
monkey.patch_all()
from gevent import Greenlet
from gevent import queue
from gevent import sleep
from threading import current_thread

from turtle.mail import connect as connect_mail
from turtle.mail import send as send_mail
from turtle.parser import query as query_info
import turtle.util


home = os.getcwd()


class SugangTurtle(object):

    def __init__(self, config):
        self.config = config
        self.emails = queue.Queue()
        self.adapters = {}

        # pushbank logger
        current_thread().name = 'MAIN'
        root_logger = logging.getLogger()
        root_logger.level = config.log_level
        log_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-5.5s]"
            " [%(threadName)s]  %(message)s")
        file_handler = logging.FileHandler('tmp/stdout.log')
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)

        school = config.SCHOOL
        if not util.verify(school):
            print "학번 정보를 정확히 입력해 주세요."
            sys.exit(1)

        s = util.get_semester()['semester']
        if s == "1R":      
            print "현재 학기는 1학기 입니다."
        else:
            print "현재 학기는 2학기 입니다."

        # log in to sugang server
        id = school['portal_account']['account']
        pw = school['portal_account']['password']
        if not parser.login(id, pw):
            print "로그인에 실패하였습니다."
            sys.exit(1)

        # connect smtp server
        self.connected = connect_mail(server=config.EMAIL['SMTP_SERVER'],
                                      port=config.EMAIL['SMTP_PORT'],
                                      user=config.EMAIL['SMTP_USER'],
                                      passwd=config.EMAIL['SMTP_PASSWORD'],
                                      tls=config.EMAIL['SMTP_TLS'])

    @staticmethod
    def start(config):
        turtle = SugangTurtle(config)
        # waiting for smtp server
        while not turtle.connected:
            sleep(0)

        tmp_path = os.path.join(home, 'tmp')
        email_process = Greenlet.spawn(turtle.handle_email)
        email_process.start()
        query_process = Greenlet.spawn(turtle.handle_course)
        query_process.start()

        try:
            gevent.joinall([email_process, query_process])
        except KeyboardInterrupt:
            print 'Sugangturtle stopped'
            sys.exit(0)

    def handle_parser(self, school, **kwargs):
        course_name = kwargs['course_name']
        current_thread().name = course_name

        kwargs['grade'] = school['grade']
        kwargs = dict(kwargs.items() + util.get_semester().items())

        result = query_info(kwargs)

        if result['success']:
            if not util.in_cache(result) and result['current'] < result['total']:
                self.emails.put({
                    'course_name': course_name,
                    'current': result['current'],
                    'total': result['total']
                })
        else:
            logging.warning("Parse failed, Reason : {0}".format(result['message']))

        # 계속해서 알랴주지 않도록 result는 저장해 놓는다
        util.save_cache(result)

    def handle_course(self):
        while True:
            course_threads = []
            for kwargs in self.config.TARGET_COURSE:

                school_info = self.config.SCHOOL
                thread = Greenlet.spawn(self.handle_parser, school_info, **kwargs)
                thread.start()
                course_threads.append(thread)

            gevent.joinall(course_threads)
            for thread in course_threads:
                del thread
            del course_threads

            sleep(self.config.REFRESH_INTERVAL)

    def handle_email(self):
        while True:
            try:
                # get recent email item
                data = self.emails.get()
                course_name = data['course_name']
                mail_title = self.config.EMAIL['TITLE'].format(course_name=course_name)
                content = util.get_content(**data)
                send_mail(target=self.config.EMAIL['TARGET'], title=mail_title,
                          content=content, course_name=course_name)
            except queue.Empty:
                # sleep zero for yield
                sleep(0)
                continue
