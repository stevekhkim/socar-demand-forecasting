# -*- coding: utf-8 -*-
"""socar_forecasting_demand_eda_v1_211031_김경현.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nJt9PUTUuiFyJOPXGLXu3DikvWFfSgIE

# 쏘카 수요지리 분석 EDA
"""

from google.colab import drive
drive.mount('/content/gdrive')

"""## 라이브러리 불러오기"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 폰트 적용
def get_font_family():
    """
    시스템 환경에 따른 기본 폰트명을 반환하는 함수
    """
    import platform
    system_name = platform.system()
    # colab 사용자는 system_name이 'Linux'로 확인

    if system_name == "Darwin" :
        font_family = "AppleGothic"
    elif system_name == "Windows":
        font_family = "Malgun Gothic"
    else:
        !apt-get install fonts-nanum -qq  > /dev/null
        !fc-cache -fv

        import matplotlib as mpl
        mpl.font_manager._rebuild()
        findfont = mpl.font_manager.fontManager.findfont
        mpl.font_manager.findfont = findfont
        mpl.backends.backend_agg.findfont = findfont
        
        font_family = "NanumBarunGothic"
    return font_family

font_family = get_font_family()

# 그래프 스타일 설정
# print(plt.style.avaiable)
# https://matplotlib.org/3.3.3/tutorials/introductory/customizing.html

# 폰트설정
plt.rc("font", family=font_family)

# 마이너스 폰트 설정
plt.rc("axes", unicode_minus=False)

# 그래프에 retina display 적용
from IPython.display import set_matplotlib_formats
set_matplotlib_formats("retina")

# 한글폰트 확인
pd.Series([1,3,5,-7,9]).plot(title="한글")

"""## 데이터 불러오기"""

data_path = '/content/gdrive/MyDrive/Data Analysis/Aiffel/HAC/03/data/20211022_sample_hackathon_data.csv'
df = pd.read_csv(data_path, encoding='cp949')
df.shape

# 반납일자 기준 오름차순 정렬
df = df.sort_values(by='reservation_return_at')
df = df.reset_index()
df = df.drop('index', axis=1)
df.head()

# 예약번호 추가(Primary Key)
reservation_number = []

for i in range(1, 457068):
  reservation_number.append(i)

df_temp = pd.DataFrame(reservation_number)

df['예약번호'] = df_temp[0]
df.head()

df.info()

"""## 테이블 정보 요약

### 1) region1 (시/도)
- 경기도, 부산광역시, 울산광역시, 세종특별자치시, 전라북도 5개 지역의 데이터

### 2) region2 (시/군/구)
- 각 시/도별 하위 시/군/구 데이터
- 부산광역시는 '강서구' 데이터만 존재
- 전라북도는 '전주시' 데이터만 존재
- 세종특별자치시는 '세종시' 데이터만 존재

### 3) reservaiton_return_at (예약반납시점)
- 차량 이용 종료시간(연-월-일, 시-분-초)

### 4) reservaiton_start_at (예약시작시점)

- 차량 이용 시작시간(연-월-일, 시-분-초)

### 5) age_group (연령대)
- 1 : 20~29세
- 2 : 30~39세
- 3 : 40~49세
- 4 : 50~59세
- 5 : 60대 이상

### 6) gender (성별)
- female : 여성
- male : 남성
- unknown : 탈퇴한 고객

### 7) car_model (차종)
- 경형, 소형, 준중형, 중형, 대형, 소형SUV, 준중형SUV, 중형SUV, 승합, 수입

## 데이터 전처리

### 결측치 확인
"""

df.isnull().sum()

"""결측치는 없는 것으로 확인되나 테이블 정보에서 gender 컬럼에 'unknown' 데이터는 결측치로 간주해야 한다."""

df['gender'].head(10)

# 성별 이용건수 현황
df['gender'].value_counts()

# unknown 데이터 삭제
print('변경 전: ', df.shape)
df = df[df['gender'] != 'unknown']
print('변경 후: ', df.shape)

df['gender'].value_counts()  # unknown 데이터가 제거되었는지 확인

"""현재 날짜 관련 컬럼의 데이터 유형이 object이므로 전처리를 위해 datetime 형태로 먼저 변환해준다."""

# 날짜 관련 데이터 유형 변경 및 전처리
df['반납일시'] = pd.to_datetime(df['reservation_return_at'], format='%Y-%m-%d %H:%M:%S')
df['반납월'] = df['반납일시'].dt.strftime('%Y-%m')
df['반납시간'] = df['반납일시'].dt.hour
df['반납요일(숫자)'] = df['반납일시'].dt.dayofweek
df['반납요일'] = df['반납일시'].dt.day_name()

df['대여일시'] = pd.to_datetime(df['reservation_start_at'], format='%Y-%m-%d %H:%M:%S')
df['대여월'] = df['대여일시'].dt.strftime('%Y-%m')
df['대여시간'] = df['대여일시'].dt.hour
df['대여요일(숫자)'] = df['대여일시'].dt.dayofweek
df['대여요일'] = df['대여일시'].dt.day_name()

"""🔎 카셰어링 데이터에 대여/반납일자 데이터에서 __종종 반납일자가 대여일자보다 빠른 경우__가 있다.   
이러한 데이터는 이용기간 계산 시 -(마이너스)로 표기가 되기 때문에 미리 전처리를 해줘야 한다.  
"""

# 이용기간 계산(시간, 일 단위)
df['이용기간'] = df['반납일시'] - df['대여일시']
df['이용기간(시간)'] = df['이용기간'].apply(lambda x: round(x.seconds / 3600 + x.days * 24, 2))
# df['이용기간(시간)'] = df['이용기간'].apply(lambda x: x.seconds // 3600 + x.days * 24)
df['이용기간(일)'] = round(df['이용기간(시간)'] / 24, 1)

print('최다 이용기간(일): ', df['이용기간(일)'].max())
print('최소 이용기간(일): ', df['이용기간(일)'].min())

# 이용기간 MAX 대여건

df[df['이용기간(일)'] == 15.2]

"""🔎 현재 데이터만으론 이상치 여부를 판단하기 어렵다. 최소 __주행거리 정보__가 있어야 이상치 여부를 가늠할 수 있다."""

# 이용기간 MIN 대여건
df[df['이용기간(일)'] == -0.7]

"""대여날짜보다 반납날짜가 더 빨라 데이터에 오류가 있는 것 같다."""

# 대여날짜보다 반납날짜가 더 빠른 경우
# 데이터 오류 18건 존재
df[df['이용기간(시간)'] < 0].shape

# 데이터 오류가 있는 18건은 삭제해줍니다.
print('변경 전: ', df.shape)
df = df[df['이용기간(시간)'] >= 0]
print('변경 후: ', df.shape)

"""## EDA(탐색적 데이터 분석)"""

df.head(10)

# 전체 예약건수 확인
total_reservations = df['예약번호'].count()  # 여러 데이터들을 시각화 했을 때 평균치를 계산하는 데 사용할 것이다.
total_reservations

"""### region1 (시 단위)"""

# 지역명칭 변경(replace)
df['region1'] = df['region1'].replace(
    ["경기도","부산광역시","울산광역시","세종특별자치시","전라북도"], 
    ["경기","부산","울산","세종","전북"]
    )

df['region1'].unique()

df['region1'].value_counts()

df['region1'].value_counts(normalize=True)

# 지역별 이용건수 시각화
plt.figure(figsize=(8,4))
g = df['region1'].value_counts().sort_values().plot.barh(title="지역별(시/도 대여건수)")
plt.text(342602, 4, '356,347')
plt.text(45377, 3, '47,103')
plt.text(26577, 2, '26,577')
plt.text(14478, 1, '14,478')
plt.text(10383, 0, '10,383')
plt.show()

"""이용건수가 많은 순으로 내림차순 정렬 하였다. 아래 지역별 시/군/구 단위 데이터를 추가로 확인해 세부적으로 어떤 쏘카존의 이용 정보가 있는지 확인한다.

### region2 (구 단위)
"""

# 데이터 공백 제거
df['region2'] = df['region2'].str.replace('　', ' ')
df['region2'].unique()

# 시/도 단위 + 시/군/구 단위 정보를 결합하여 전처리
df['region3'] = df['region1'] + " " + df['region2']
df['region3'] = df['region3'].str.replace('　', ' ')

# 우선, 시/군 단위 정보는 포함하고, 구 단위 정보는 제외하는 전처리
df['region3'] = df['region3'].replace(
    ['경기 고양시 덕양구', '경기 성남시 분당구', '경기 성남시 수정구',
       '경기 성남시 중원구', '경기 안양시 동안구', '경기 안양시 만안구', '전북 전주시 덕진구',
       '전북 전주시 완산구', '경기 고양시 일산동구', '경기 고양시 일산서구'],
    ['경기 고양시', '경기 성남시', '경기 성남시',
     '경기 성남시', '경기 안양시', '경기 안양시', '전북 전주시',
     '전북 전주시', '경기 고양시', '경기 고양시']
)

# 지역별(상세) 이용건수 시각화
g = df['region3'].value_counts().sort_values().plot.barh(figsize=(8,6), title='지역별 대여건수(상세)')

"""- region1 컬럼 데이터만 확인 했을 때 부산보다 울산 지역의 이용건수가 많았던 이유는, 울산은 5개 구 정보의 이용 데이터가 있으나 부산 이용건수 데이터가 '부산시 강서구'로 한정되었기 때문이다.
- 전라북도의 경우에도 오직 전주시 데이터 밖에 없음에 참고가 필요하다.

🔎 __지역별 쏘카존 정보 테이블이 있었으면 '지역별 이용건수 / 쏘카존 개수'를 계산해 상대적 비교가 가능 했을 것이다.__

### reservation_return_at (예약 반납시점)
"""

# 월별 반납건수
df['반납월'].value_counts().sort_index().plot.bar(figsize=(10,6), title="월별 반납건수")
plt.axhline(y=total_reservations / 11, c='r', lw=0.5) # 전체 반납건수 / 12 (=12개월)
plt.show()

"""대여건수가 가장 많은 월은 7월, 10월 이지만 단순히 월별 이용건수로는 시사점을 찾기가 힘들다.
- 10월에 이용건수가 많았던 것은 추석 연휴가 있을까 생각해보았으나 __2019년 추석은 9월__이었다.
- __시간의 흐름에 따라 쏘카에서 운영하는 차량대수가 늘어나 자연스레 이용건수가 늘었을 것으로 추측해볼 수도 있다.__

🔎 카셰어링 사업은 __시즈널한 이슈가 있기 때문에 차량의 신규투입, 매각 등으로 차량 대수를 인위적으로 조정__한다.   
   월별 이용건수의 많고 적음을 판단하기 위해서는 월별 해당 지역의 __차량 운영대수 정보__를 확인해볼 필요가 있을 것이다.
"""

# 요일별 반납건수
df['반납요일(숫자)'].value_counts().sort_index().plot.bar(figsize=(8,6), title='요일별 반납건수')
plt.axhline(y=total_reservations / 7, c='r', lw=0.5)  # 전체 반납건수 / 7 (=1주일)
plt.show()

"""0은 월요일, 1은 화요일, 2는 수요일, 3은 목요일, 4는 금요일, 5는 토요일, 6은 일요일을 의미한다.
- 일반적으로 생각할 수 있는 것처럼 평일보다 주말의 반납 건수가 많다. 그리고 토요일보다 일요일에 반납 건수가 더 많다.
"""

# 시간대별 반납건수
df['반납시간'].value_counts().sort_index().plot.bar(figsize=(12,6), title="시간대별 반납건수")
plt.axhline(y=total_reservations / 24, c='r', lw=0.5)  # 전체 반납건수 / 24 (=24시간)
plt.show()

"""14시부터 00시까지는 평균 대비 반납 건수가 많으며, 01시부터 13시까지는 평균 대비 반납 건수가 적다.

### reservation_start_at (예약 시작시점)
"""

# 월별 대여건수
df['대여월'].value_counts().sort_index().plot.bar(figsize=(10,6), title="월별 대여건수")
plt.show()

# 요일별 대여건수
df['대여요일(숫자)'].value_counts().sort_index().plot.bar(figsize=(8,6), title='요일별 대여건수')
plt.axhline(y=total_reservations / 7, c='r', lw=0.5)
plt.show()

"""반납건수 그래프와 달리 일요일보다는 토요일의 대여건수가 더 많다."""

# 시간대별 대여건수
df['대여시간'].value_counts().sort_index().plot.bar(figsize=(12,6), title="시간대별 대여건수")
plt.axhline(y=total_reservations / 24, c='r', lw=0.5)
plt.show()

"""- 8시부터 22시 사이에는 평균 대비 대여건수가 많다.
- 주로 __오전에 대여가 가장 많은 것__을 확인할 수 있고, 오후를 지나 __저녁 시간대에 다시 대여 건이 증가__한다.
"""

# 이용기간(시간)에 따른 기술통계 - 평균, 중앙값 중심 확인
df['이용기간(시간)'].describe()

"""- 예약건당 평균 이용시간은 7.9시간, 중앙값은 4.0시간이다."""

plt.figure(figsize=(16,4))
sns.boxplot(data=df, x='이용기간(일)').set_title("이용기간 기술통계 정보")
plt.show()

# 이용기간(시간)에 따른 기술통계 - 평균, 중앙값 중심 확인
df['이용기간(일)'].describe()

"""데이터상으로 대여기간이 8시간을 초과하게 되면 이상치로 볼 수 있다.

이용시간을 12시간으로 기준점을 잡고, 이를 초과하는 데이터를 장기 대여로 간주해 다양한 방식으로 시각화를 진행해본다.
"""

df['이용기간_구분'] = 0
df.loc[df['이용기간(일)'] <= 0.5, '이용기간_구분'] = 1  ## 이용시간 12시간 이하
df.loc[df['이용기간(일)'] > 0.5, '이용기간_구분'] = 2  ## 이용시간 12시간 초과
df['이용기간_구분'].value_counts()

# 이용시간에 따른 지역별 특성 시각화
sns.catplot(data=df, y="이용기간_구분", kind="count", col="region1", col_wrap=2)
plt.show()

pd.crosstab(df['region1'], df['이용기간_구분'], normalize='index')

"""- 다른 도시에 비해서 부산(강서구)의 이용시간이 긴 대여건이 많음을 알 수 있는데, 부산시 강서구에 김해국제공항이 위치해 있다.
- 세종시의 경우 이용시간이 12시간을 초과하는 대여건이 가장 적은 것을 알 수 있다. (장기 이용의 필요성이 적은 지역?)
"""



# 요일에 따라서 지역적으로 차량 이용건수의 패턴이 다른 곳이 있을까? (EX. 세종시)
sns.catplot(data=df, y="대여요일(숫자)", kind="count", col="region1", col_wrap=2)
plt.show()

pd.crosstab(df['대여요일(숫자)'], df['region1'])

"""- 부산의 경우 토요일보다 금요일 이용건수가 더 많다.
- 전주, 울산, 세종 모두 토요일 이용건수가 가장 많지만, 경기도와 비교 했을 때 평일과 주말 이용건수가 엄청난 차이를 보이는 것은 아니다.
"""

# 요일에 따라 이용하는 차종의 패턴이 다른 경우가 있을까?
sns.catplot(data=df, y="car_model", kind="count", col="대여요일(숫자)", col_wrap=2)
plt.show()

# 요일에 따라 빌리는 빌리는 시간대가 다를까?
sns.catplot(data=df, y="대여시간", kind="count", col="대여요일(숫자)", col_wrap=2)
plt.show()

"""평일과 주말(토요일)의 주력 대여시간대가 조금 차이가 있음을 알 수 있다.

### age_group (연령대)
- 1 : 20대
- 2 : 30대
- 3 : 40대
- 4 : 50대
- 5 : 60세 이상
"""

df['age_group'].value_counts()

df['age_group'].value_counts(normalize=True)

df['age_group'].value_counts().plot.bar(rot=360, title="연령대별 이용건수")
plt.show()

"""20~30대 이용고객이 전체 이용건수의 약 85%를 차지하고 있다."""

# 대여시간대에 따라 빌리는 연령대가 다를까?
sns.catplot(data=df, y="대여시간", kind="count", col="age_group", col_wrap=2)
plt.show()

"""20대의 경우 18시이후부터 00시까지 저녁시간대의 이용건수가 다른 연령대에 비해 많음을 알 수 있다."""

# 지역에 따라 이용 고객의 연령대가 달라질까?
sns.catplot(data=df, y="age_group", kind="count", col="region1", col_wrap=2)
plt.show()

sns.catplot(data=df, y="age_group", kind="count", col="region3", col_wrap=2)
plt.show()

"""- 거의 모든 지역에서 20대의 이용건수가 가장 많았으며, 30대의 이용건수가 가장 높았던 곳은 부산 강서구, 울산 울주군 2개 지역이 있다

### gender (성별)
- female : 여성
- male : 남성
"""

df['gender'].value_counts()

df['gender'].value_counts(normalize=True)

df['gender'].value_counts().plot.bar(rot=360, title="성별 이용건수")
plt.show()

"""- 앞에서 전체 이용 객중 약 4% 정도의 탈퇴 고객을 결측치로 간주하고 전처리 해주었다. 
- 이용건수 중 남성과 여성의 비율을 4대1 정도로 확인된다.
"""

# 성별에 따라 선호하는 차종이 다를까?
sns.catplot(data=df, y="car_model", kind="count", col="gender", col_wrap=2)
plt.show()

"""남성이 가장 많이 이용한 차종은 준중형, 여성이 가장 많이 이용한 차종은 경형이다.

### car_model (차종)
"""

df['car_model'].unique()

df['car_model'].value_counts()

df['car_model'].value_counts(normalize=True)

df['car_model'].value_counts().sort_values().plot.barh(figsize=(10,6), title='차종별 이용건수')
plt.show()

"""🔎 단기렌터카 시장에서는 소형SUV, 준중형SUV의 가격 경쟁력이 떨어지는 편이다. 하지만 카셰어링 시장에서는 이용건수가 많은 것을 확인할 수 있는데 대여건수가 많은 이유는 경형, 준중형 만큼 가격 경쟁력이 있다는 것일까?
- 쏘카 요금표에서 가격 정보 확인 필요
"""

# 연령대별/차종별 이용 비중
pd.crosstab(df['age_group'], df['car_model'], normalize='columns')

"""- 20대 주력이용 차종 : 경형, 소형, 준중형, 소형 SUV
- 대형, 승합, 중형SUV의 경우 30~40대의 이용 비중이 20대보다 많다.
"""

# 지역에 따라 차종 이용 특성이 다를까? (예를 들어 공공기관이 많은 세종시)
sns.catplot(data=df, y="car_model", kind="count", col="region1", col_wrap=2)
plt.show()

sns.catplot(data=df, y="car_model", kind="count", col="region3", col_wrap=2)
plt.show()