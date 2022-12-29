# autodriving_robot
# 자율주행로봇 / 모니터링 부

### 1. 프로젝트 목표

- 모터 제어 + 라이더 센싱 + 모니터링 및 원격 제어
- 동의대 전자과 6층 건물 자율주행 시연 목표
- 자율주행 중 장애물 인식과 회피 기능, 목적지까지 자율주행, 자율주행 중 원격 모니터링, 긴급 상황의 경우 원격 제어

### 2. 제작 기간 / 참여인원

- 2021-03 ~ 2022-08 / 전자공학 전공 3명

### 3. 사용한 기술 스택

#### 언어 및 프레임워크

- Python
- HTML/CSS/JaveScript
- OpenCV 라이브러리
- Flask 라이브러리

#### 개발환경

- Ubuntu 20.04LTS
- Window 
- Visual Studio Code
- SSH
- GitHub

### 4. 나의 역할

- 카메라를 활용한 객체 인식 (목적지 도착 시 해당 사용자 인식)
- 실시간 모니터링
- 원격 모터 제어
- 실시간 주행속도 그래프 표시 
- 기능 구현을 위한 웹 개발

### 5. 핵심기능

1. 로봇 자율주행 시 원격에서 로봇 주행 상황을 실시간 모니터링 (스트리밍 + 주행속도)
2. 긴급 상황 시 원격 제어 기능 가능
3. 목적지 도착 후 사용자 인식을 통한 정보 일치 확인

#### ※ 기능구현

- BackEnd 구현 : Flask <-> FrontEnd 구현 : Html/CSS/JavaScript

  > 구상도

  <img width="474" alt="image" src="https://user-images.githubusercontent.com/84834776/194814766-e776cee8-91b7-42ad-b64c-bf6afeeb43b3.png">

- OpenCV + 얼굴 인식 시스템(Face Recognition) 활용하여 목적지 도착 후 사용자 일치 확인

  > 오바마, 바이든, 나의 얼굴 저장 후 해당 객체 얼굴 인식 결과

  <img width="243" alt="image" src="https://user-images.githubusercontent.com/84834776/194809968-e2f2d529-ba2f-4e5d-a06a-60d5dae28fc6.png">

  *** TMI 이 활동을 계기로 처음 데이터 분석 및 머신러닝/딥러닝에 관심을 가짐. ***
  
- 원격 제어 및 주행 속도 데이터 모니터링

  > 버튼 입력을 통한 모터 제어와 주행 속도 변화 그래프

  <img width="261" alt="image" src="https://user-images.githubusercontent.com/84834776/194810463-7d9e853f-2cba-4521-befb-517daabaebee.png">

  * 1초에 한번씩 속도 값 반환
  * 버튼 입력 시 방향 제어 가능
  
### 6. 트러블 슈팅

- 처음 접해본 웹 개발

  > Problem
  
  처음엔 네트워크 포트포워딩을 통한 외부접속으로 앱 개발을 하려고 하였으나, 학교 통신 보안 상 포트포워딩이 불가.
  
  > Solution
  
  웹 개발을 통해 구현.
  
  Python Flask를 활용한 웹 서버 구축 관련 도서 참고 및 구글링, 더하여 웹을 구현하기 위해 필요한 html/css/Java Script 공부 

- 라이더와 모니터링의 통합 작업

  > Problem

  라이더로 센싱된 값을 웹에서 표시해주기 위한 개발의 어려움. 
  
  내부적으로 데이터를 받아와 웹으로 표현하려하였으나, 웹 표현을 위한 데이터 형식 변환 작업의 어려움.

### 7. 동작 영상 YouTube 링크

  [시연영상 Click](https://youtu.be/Vu4WY2ludRw)
