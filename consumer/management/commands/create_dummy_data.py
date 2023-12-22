from accounts.models import User
from django.contrib.auth import get_user_model
from consumer.models import Resume

User = get_user_model()

전홍식 = User.objects.create_user(name="전홍식", password="password")
연창현 = User.objects.create_user(name="연창현", password="password")
홍채우 = User.objects.create_user(name="홍채우", password="password")
박준희 = User.objects.create_user(name="박준희", password="password")
조은성 = User.objects.create_user(name="조은성", password="password")


Resume1 = Resume.objects.create(
    author=전홍식,
    call="010-4565-9847",
    gender="male",
    age="26",
    education="평양대 정치과",
    career="신공화당 총재",
    award="노벨독재상",
    introduce="바이든 개새끼",
)

Resume2 = Resume.objects.create(
    author=연창현,
    call="010-5469-8428",
    gender="male",
    age="23",
    education="동경대 침략과",
    career="천왕 시다바리",
    award="대일본제국 앞잡이상",
    introduce="조선총독부 재건 기원",
)

Resume3 = Resume.objects.create(
    author=홍채우,
    call="010-5476-3644",
    gender="female",
    age="23",
    education="상트페테르부르크 국립대 인구정리과",
    career="유대인 가스실 감독관",
    award="나치 실험우수상, 스탈린 대학살우수상, KKK 차별우수상, 전두환 지지상",
    introduce="'난 흑인이 jail 싫어'",
)

Resume4 = Resume.objects.create(
    author=박준희,
    call="010-6637-5143",
    gender="gay",
    age="23",
    education="미시시피주립대 평등과",
    career="여성가족부 장관 후보, 맨체스터유나이티드 2부 강등 감독",
    award="여성전용주차구역 설치상, 지구환경보호시위 모나리자훼손상, 비건지지 육식차별상, 길고양이 품종 확대상, 세계게이의날 우수참여상",
    introduce="연창현 감금하고싶다",
)

Resume5 = Resume.objects.create(
    author=조은성,
    call="010-9924-7987",
    gender="male",
    age="25",
    education="uneducated kid",
    career="none",
    award="엑셀 C급",
    introduce="여러분",
)
