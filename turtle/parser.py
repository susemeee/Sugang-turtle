# -*- coding: utf-8 -*-
import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

logged_in = False
session = requests.Session()

def login(snumber, password):
    global logged_in
    if not logged_in:
        url = "https://sugang.korea.ac.kr/LoginAction.jsp"
        params = {
            "id" : snumber,
            "pw" : password
        }
        success, data = get_data(url, params, method="POST", referer="http://sugang.korea.ac.kr/SugangLogin.html")

        if u"학번 또는 암호가 틀리거나 존재하지 않습니다" in data:
            success = False
        else:
            logged_in = True
            success = True

        return success
    else:
        print "already logged in"

def query(request):
    global logged_in
    message = ""
    
    if logged_in:
        info_url = "http://sugang.korea.ac.kr/lecture/LecLmtInfoUniv.jsp?courcd={0}&courcls={1}&year={2}&term={3}"
        info_url = info_url.format(request['course_id'], request['class'], request['year'], request['semester'])
        success, data = get_data(info_url)
    else:
        success = False
        message = "Not logged in"

    d = {
        'success' : success,
        'message' : message
    }
    if success:
        data = data.replace('&nbsp;', '')
        data = BeautifulSoup(data)

        try:
            data = data.select('table')[0]

            if all([trim(data.select('td:nth-of-type({0})'.format(i*3))[0].text) == u"-" for i in range(1,5)]):
                # 정원만 보면 됨
                cols = data.select('tr')[-1].select('td')
            else:
                # 아니면 학년을 보던가
                cols = data.select('tr')[request['grade']].select('td')

            d['current'] = int(trim(cols[1].text))
            d['total'] = int(trim(cols[2].text))

        except IndexError:
            d['success'] = False
            d['message'] = "잘못된 학수번호를 입력하였습니다."

    return d

def trim(string):
    return string.replace("\r", "").replace("\n", "").replace("\t", "").strip(' ')

def get_data(url, params={}, method="GET", referer=None):
    try:
        if referer:
            session.headers.update({'Referer' : referer})

        # 고려대학교 수강신청 시스템은 신뢰하지 않는 Root CA를 사용하기 때문에, SSL Verification 끔
        if method == "GET":
            data = session.get(url, params=params, verify=False).text
        elif method == "POST":
            data = session.post(url, params=params, verify=False).text


        success = True
    except Exception, e:
        print e
        success = False
        data = None
        # if e.getcode() == 500:
        #     data = e.read()
        
    return success, data

