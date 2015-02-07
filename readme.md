# Sugang Turtle 

수강신청 공좌석 알림 시스템

## 개요

수강 정정 시, 자리가 생긴 과목을 알고 싶으세요? 그렇다고 항상 컴퓨터를 쳐다볼 수도 없고...

이 프로그램은 **바쁜 나를 대신하여** 수강정정 때 빈 자리가 생기는 과목을 메일로 알려줍니다.

Gmail 앱과 같이 사용하면 금상첨화!

## 사용하는 법

### 1. Python을 설치합니다. 
* Sugang Turtle은 Python 2.7.x에서 동작합니다.
* [https://www.python.org](https://www.python.org) 

### 2. 의존하는 라이브러리를 설치합니다.

1) pip를 설치합니다. [https://pip.pypa.io/en/latest/installing.html](https://pip.pypa.io/en/latest/installing.html)

(Python 2.7.9부터는 pip가 설치되어 있기 때문에 설치하지 않으셔도 됩니다.)

2) SugangTurtle이 있는 곳으로 현재 디렉터리를 옮깁니다.
	
3) 다음 명령어를 터미널(또는 명령 프롬프트)에서 실행합니다. `pip install -r requirements.pip`

### 3. SugangTurtle을 실행하여 기본 설정 파일을 만듭니다.

`python ./turtle.py`를 입력하면, config.py라는 설정 파일이 생깁니다. 이 config.py를 적절히 수정하여 교내 포탈 정보와 지켜 볼 과목의 정보를 입력합니다.

### 4. SugangTurtle을 다시 실행합니다.

이제 지켜 볼 과목 목록의 빈 자리가 생기면 지정된 메일로 알려줍니다!

## 지원

- 이 프로그램은 [PushBank](https://github.com/ssut/PushBank)를 기반으로 만들어졌습니다.

- 프로그램에 대한 문의는 제작자 [https://fb.com/susemeee](https://fb.com/susemeee)로 해주세요.

- SugangTurtle은 MIT 라이센스를 따릅니다.


