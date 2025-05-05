#Realtime-Detector

이 프로젝트는 다음과 같은 내용을 포함합니다:

-Nudenet : ytb_server.py 와 그 부속 파이썬 코드가 포함된 폴더로, 실행은 ytb_server.py를 하면 됩니다.
-chrome_extension_1 : 사용자가 영상을 클릭 시에 자동으로 해당 영상을 flask server로 다운을 시작합니다.
-chrome_extension_2 : ytb_server.py에서 nudity detect가 되고, 해당 감지된 프레임을 json파일로 반환할 시, 이를 수신하여 사용자가 재생중인 영상 내에서 해당 프레임에 가기 직전 영상을 멈추고, 

## 실행방법 ##
1. pip install -r NudeNet/requirements.txt
2. google chrome 접속
3. 주소창에 chrome://extensions 입력 후 접속
4. 우측상단에 개발자모드 on
5. 압축해제된 확장프로그램을 로드합니다 클릭
6. realtime-detector에 접근 후 , chrome_extension_1 폴더 선택
7. 마찬가지의 방법으로 chrome_extension_2 폴더 선택
8. Nudenet 내부의 ytb_server.py 실행
9. 구글 크롬에서 유튜브 접속 후 영상 재생