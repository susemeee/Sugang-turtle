#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
Sugang Turtle - Notification for available sugang seat

Copyright (c) 2014 Suho Lee.

Licensed under the MIT License.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""
from textwrap import dedent

import logging
import os
import sys

def create_default_config(fn):
    f = open(fn, 'w')
    f.write(("""\
#-*- coding: utf-8 -*-
EMAIL = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    # 이메일을 보낼 구글 ID를 입력합니다.
    'SMTP_USER': '',
    # 비밀번호를 입력합니다.
    'SMTP_PASSWORD': '',
    'SMTP_TLS': True,
    # 받을 이메일 주소를 입력합니다.
    'TARGET': '',
    'TITLE': u'{course_name} 과목 신청 가능 안내',
}

SCHOOL = {
    'portal_account': {
        # 학번을 입력합니다.
        'account': '',
        # 포탈 비밀번호를 입력합니다.
        'password': ''
    },
    # 학년을 입력합니다.
    'grade': 2
}

# 지켜 볼 학수번호를 입력합니다.
# [주의] course_name 항목 앞에는 u가 붙어야 합니다.
TARGET_COURSE = [
    {
        'course_id': 'SPGE195',
        'course_name': u'Campus CEO 2.0(Ⅱ)',
        'class': '00'
    },
    {
        'course_id': 'COSE211',
        'course_name': u'이산수학(영강)',
        'class': '01'
    }
]

# 갱신 주기 (초 단위) 를 입력합니다.
REFRESH_INTERVAL = 30
"""))
    f.close()


def _import(code, name, add_to_sys_modules=0):
    """
    Import dynamically generated code as a module. code is the
    object containing the code (a string, a file handle or an
    actual compiled code object, same types as accepted by an
    exec statement). The name is the name to give to the module,
    and the final argument says wheter to add it to sys.modules
    or not. If it is added, a subsequent import statement using
    name will return this module. If it is not added to sys.modules
    import will try to load it in the normal fashion.

    import foo

    is equivalent to

    foofile = open("/path/to/foo.py")
    foo = importCode(foofile,"foo",1)

    Returns a newly generated module.
    """
    import sys,imp

    module = imp.new_module(name)

    exec code in module.__dict__
    if add_to_sys_modules:
        sys.modules[name] = module

    return module


def main():
    config_file = os.path.join('.', 'config.py')
    tmp_dir = os.path.join('.', 'tmp')
    if not os.path.isfile(config_file):
        create_default_config(config_file)
        print 'Created config file. Edit config.py and run turtle again'
        sys.exit(0)
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir, 0777)

    try:
        f = open("config.py").read()
        config = _import(f, "config", 1)
    except: 
        print 'Error: Could not import a config file!'
        sys.exit(1)

    import optparse
    optp = optparse.OptionParser()
    optp.add_option('-v', '--verbose', dest='verbose', action='count',
                    help="Increase verbosity"
                    "(specify multiple times for more)")
    opts, args = optp.parse_args()

    log_level = logging.WARNING
    if opts.verbose == 1:
        log_level = logging.INFO
    elif opts.verbose >= 2:
        log_level = logging.DEBUG

    config.log_level = log_level

    from turtle import SugangTurtle
    SugangTurtle.start(config)

if __name__ == "__main__":
    main()
