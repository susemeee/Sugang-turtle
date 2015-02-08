#-*- coding: utf-8 -*-
from datetime import datetime
import sys

def get_semester():
    now = datetime.now()

    year = now.year
    month = now.month

    if month in [12, 1, 2, 3, 4, 5, 6]:
        semester = "1R"
    elif month in [7, 8, 9, 10, 11]:
        semester = "2R"

    return {"semester" : semester, "year" : year}


def verify(school):
    if not school['portal_account']['account']:
        return False
    elif not school['portal_account']['password']:
        return False
    elif not school['grade']:
        return False

    return True

def encode(string):
    if sys.stdout.encoding == "cp949":
        return string.encode("cp949")
    else:
        return string.encode("utf-8")

def get_content(course_name, current, total):
    return u"""
<html>
<head>
<style>
    body {{
        font-size: 14px;
        font-family: 'Apple SD Gothic Neo', NanumGothic, 'Malgun Gothic';
    }}
</style>
</head>
<body>
    <p>{0} 과목의 신청이 가능해졌으니 확인 부탁드립니다.</p>
    <p>현재 인원 : {1}명</p>
    <p>정원 : {2}명</p>
    <p><a href="http://sugang.korea.ac.kr">수강신청 홈페이지 접속하기</a></p>

</body>
</html>""".format(course_name, current, total)

c = []

def save_cache(obj):
    global c
    c.append(obj)

def in_cache(obj):
    return obj in c