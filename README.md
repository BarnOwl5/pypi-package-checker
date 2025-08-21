# PyPI Package Checker [WIP]
Updated at 2025.08.21
## 1. About
PyPI Package Checker는 PyPI API를 활용해 입력한 패키지가 실제로 존재하는지와 최신 상태를 간단히 확인할 수 있는 CLI 도구입니다.

LLM이 존재하지 않는 패키지를 추천하는 ‘환각’ 현상을 보며, 실제 보안 문제로 이어질 수 있는 슬롭 스쿼팅(Slop Squatting) 공격 가능성을 체감했습니다. 이를 예방하기 위해 사용자가 직접 패키지 존재 여부와 최신 업데이트 상태를 검증할 수 있도록 본 프로젝트를 진행했습니다.

## 2. 주요 기능
AI가 추천해주는 패키지 이름이 모호하다면 사용자는 언제든지 패키지의 존재여부와 최신 업데이트 상태를 확인할 수 있습니다.

- 입력한 PyPI 패키지 존재 여부 확인
- 패키지의 마지막 업데이트 날짜 조회
- 패키지 깃허브 주소, summary, 이메일 유무 확인
- 조회 결과를 '.json' 형식으로 자동 저장
- 히스토리 목록 확인 (저장된 결과 파일 목록)
- 최근 조회한 3개 패키지 자동 표시

## 3. 설치 방법
- Python 권장 버전 : 3.10 이상
- 이 프로젝트는 현재 GitHub 저장소에서만 배포되고 있으며, 별도의 설치 패키지는 제공하지 않습니다.
- 필수 라이브러리 : os, sys, json, requests, re, time, getpass

<pre><code>
  git clone https://github.com/BarnOwl5/pypi-package-checker.git
  cd pypi-package-checker
  
  python3 terminal.py
</code></pre>

## 4. 실행 시 사용 방법
### 4-1. 메인 메뉴
- 프로그램 실행 직후 출력되는 메뉴

<img src="/SourceCode/images/1.main_menu.png" width="450px" height="300"></img>
### 4-2. [1] 패키지 확인
- 패키지 이름 입력 -> 존재 여부 및 마지막 업데이트 결과 출력

<img src="/SourceCode/images/2.package_check2.png" width="450px" height="300"></img>
### 4-3. [2] 조회 내역 확인
- 저장된 .json 파일 목록 확인 및 선택 시 상세 내용 출력

<img src="/SourceCode/images/3.history2.png" width="450px" height="300"></img>
### 4-4. [3] 도움말 보기
- 프로젝트 제작 의도와 CLI 명령 안내가 포함됩니다.
  
<img src="/SourceCode/images/4.helptut.png" width="450px" height="300"></img>
## 5. 유지 및 피드백
프로젝트는 현재 완성된 상태지만, 필요 시 언제든지 기능을 추가하거나 수정할 계획입니다.
- 코드에 대한 피드백은 언제든 부탁드립니다.
- 현재는 개인 프로젝트로 관리 중입니다.

## 6. 라이센스 및 보안 안내
이 프로젝트는 Apache 2.0에 따라 배포되며, 무단 배포 및 변조는 삼가주시길 바랍니다.

- 본 도구는 학습, 확인, 연구용으로 제작되었으며 악의적인 사용, 자동화 공격, 또는 허위 패키지 유포 등에 사용해서는 안됩니다.
- 사용에 따른 모든 책임은 사용자 본인에게 있으며, 개발자는 사용 결과로 인한 손해에 대해 책임지지 않습니다.

### This tool is intended for educational and security research purposes only.
