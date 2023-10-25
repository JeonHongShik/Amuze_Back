# Amuze_Back
무용플랫폼 출시 프로젝트의 백단


python / git 설치
extension django 설치


가상환경 설치 및 가상환경 들어가기

1. 터미널 열기
2. python -m venv {가상환경이름}
3. source {가상환경이름}/scripts/activate

※ 안될경우 폴더 명 직접 들어가서 activate 하기

가상환경 들어가면 주소값 앞에 ({가상환경이름}) 뜸
 (venv) pc@DESKTOP-UGR375L MINGW64 ~/Desktop/Amuze_Back  -- 이런식으로

가상환경 들어가면 
pip install -r requirements.txt 하기

※ 프레임워크 더 설치하면 깃 커맨트에다가 뭐 설치했다고 말하고
pip freeze > requirements.txt 이거 한번 해주세요


서버 여는법
python manage.py runserver

venv 는 .gitignore 에 설정해놔 깃헙에 안올라갑니다.
