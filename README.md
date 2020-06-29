<p align="center">
  <img alt="Job Alert" title="Job Alert" src="./assets/logo.png" width="128">
</p>

<h1 align="center">Job Alert</h1>

<p align="center">
  <a href="#overview">Overview</a> |
  <a href="#features">Features</a>
</p>

## Overview

여러 사이트의 정보를 모아 메일 또는 슬랙으로 알려주는 채용 알림 서비스

## Environment

| Environment Variable                 | Development Default                          | Production Default        |
| ------------------------------------ | -------------------------------------------- | ------------------------- |
| SENDGRID_API_KEY                     |  n/a                                         | raise error               |

## Features

- [x] 채용 정보 크롤링
- [x] 신규 채용 등록 시 알림
- [x] 태그 검색 알림 등록
- [x] 이메일 전송
- [ ] 슬랙 전송

## TODO Sites

- [x] [로켓펀치](https://www.rocketpunch.com/)
- [ ] [원티드](https://www.wanted.co.kr/)

## TODO

- [ ] HTML Template to [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)
- [ ] Exception 들을 모두 커스텀하여 만들고 싶습니다. 
- [ ] 에러가 날 만한 곳은 모두 BaseException 으로 묶어놓고 로깅하여 사용하고 싶습니다.
- [ ] BaseException 에러는 로깅되고 Exception 과 TEST 를 생성하려 합니다.
- [ ] 코드 관리 툴을 넣고자 합니다. (black, flake8, isort, mypy)
- [ ] TEST Coverage 를 모두 채우려합니다. (pytest, coverage)
