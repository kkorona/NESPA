# NESPA(advaNced Evaluation System for Programming Assignment)

PNU ALgorithm & Data Engineering Lab.(지도교수 조환규) 에서 강의에 사용하는 과제 채점 사이트입니다.

프로그래밍 과제의 채점 및 관리를 지원합니다.

## Specifications
|대상|특징|
|---|---|
|Web Framework|Django|
|DB|SQLite|

## 지원 기능

*	표준 입출력(stdin, stdout) 지원
*	채점 데이터 탄력적 지원(20개 이상)
*	Python3.7 지원
* 제출된 소스코드 확인 기능 추가
*	경과 시간 출력
* 과제 제출 진행상황 확인 기능
*	확장 소스 파일(여러 개의 외부 헤더 파일, 파이썬 추가 모듈) 지원
* 강의계획표 확인 기능 (PDF viewer 또는 HTML document 선택)
* 과제별 성적을 산출하여 xls 파일로 출력
* 강의 진행을 위한 공지 / 자유 / 질문 게시판 등 지원(마크다운 편집기)

## 지원 예정 기능

*	Grading System 사용 가능(차등 배점 및 성적 표시 기능) 선택적 사용
*	Assembly를 비롯한 기존 취약점 보완
*	메모리 사용량 출력
* 채점 기록 초기화 기능 추가
* DOM Judge 연동 예정, 교내 대회 및 시험에 활용할 수 있음
* 비동기 채점 기능 - 채점 진행 상황을 사용자가 확인 가능
* 소스코드 DNA 기반 과제 표절 검사 기능
* 다중 강의 관리 시스템 


## 추가 미정 기능

* Go, Rust 지원
* back-up 기능 개선


# Progrss 2022. 02. 04.
다중 강의 시스템 지원을 위한 소스코드 통합 작업 진행중 
