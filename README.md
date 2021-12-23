# AIFFEL X SOCAR PROJECT
- 모두의연구소 산하 인공지능 교육기관 AIFFEL과 카셰어링 기업 SOCAR가 협력하여 진행된 기업 연계 해커톤 프로젝트로서, [미시적 수요 분석과 모델링] 주제에 대해 SOCAR로부터 제공 받은 예약 데이터를 기반으로 프로젝트를 진행하였습니다. 
- 단, SOCAR 제공 데이터 EDA 및 시각화 자료는 저작권 및 보안 이슈 문제로 비식별화 처리 되었음을 참고 바랍니다.  


## 1. 프로젝트 소개
### 개요
- 주제 : **지역적 특성과 날씨 요소를 고려한 수요예측 분석**  
- 기간 : 2021.11.10(수)  ~ 2021.12. 15(화)  
- 방식 : 팀 프로젝트  
- 구성원 

| 이름   |  구성   |                      역할                  |
| :----: | :----: |  :---------------------------------------: | 
| 최선웅   |  팀장   | 프로젝트 총괄, 외부 데이터 수집, EDA, FE, 모델링 구현   | 
| 김경현  |  팀원   | 외부 데이터 수집, EDA, FE, PPT 작성, 마케팅 포인트 도출   | 
| 문소정  |  팀원   | 외부 데이터 수집, EDA  | 
| 이서윤  |  팀원   | 외부 데이터 수집, EDA, PPT 총괄, QGIS, 마케팅 포인트 도출 | 

### 기술 스택
- Google Colaboratory, Pandas, Matplotlib, Seaborn, Scikit-learn 외

### 문제정의
- 카셰어링 수요는 지역, 계절, 요일 특성에 따라 다양한 패턴을 보임
- 날씨가 고객의 이용 목적과 수요를 파악하는데 있어 어떠한 영향을 미치는지 탐색하고자 함  

![img11](https://user-images.githubusercontent.com/83560273/147148093-f696549f-4e7b-48df-9152-0e3ece20b124.JPG)

### 프로젝트 목표
- 지역과 날씨가 카셰어링 수요에 얼마나 영향을 미치는지 파악 후 비즈니스에 적용 가능한 개선 포인트 도출
- 이용건수가 아닌 실제 매출에 직접적으로 영향을 미치는 **이용시간**을 **타겟변수로 설정**

![img12](https://user-images.githubusercontent.com/83560273/147148095-2d7602d8-177e-4af4-8a2c-5617191d0876.JPG)

### 프로세스

![img13](https://user-images.githubusercontent.com/83560273/147153888-1901f71e-e42b-446d-9e7c-9ccc9845d501.JPG)

## 2. 프로젝트 내용

### 데이터 분석(EDA) 및 전처리
- 지역적 특성
  - 공항/역사 주변 쏘카존의 경우 요일별/연령대별 이용량이 다른 지역과 차이를 보임
  
  ![img21](https://user-images.githubusercontent.com/83560273/147155809-e0459f21-5529-4aa6-9607-ca113ca37577.JPG)
  
  - 공항/역사 주변 쏘카존의 경우 평일과 30대 이용량이 높게 나타남 → 출장 수요 유추 가능
  
  ![img22](https://user-images.githubusercontent.com/83560273/147155796-85eace0b-4c8f-47ba-8d36-e9a5dd30869b.JPG)
  
- 날씨
  - 지역별 강수량에 따른 이용패턴의 차이 존재: 강수량이 많을수록 절대 이용시간 감소
  
  ![img23](https://user-images.githubusercontent.com/83560273/147155799-57b043b3-2302-4319-8402-957a3ff13005.JPG)
  
  - 연속적으로 비가 오는 날에 총 수요시간 평균에 차이 발생(T-Test)
  
  ![img24](https://user-images.githubusercontent.com/83560273/147155801-f952bf45-3bf7-4b15-98b4-0f4a26da42d6.JPG)
  
  - 3~4일 비가 연속적으로 내리는 경우 주말 수요량이 줄어듦을 확인할 수 있음
  
  ![img25](https://user-images.githubusercontent.com/83560273/147155802-b1afa858-f18b-47b1-8ec7-1d7b9f7c39c4.JPG)
    
    
- 공휴일
  - 공휴일과 주말 사이에 평일 이용시간이 공휴일이 없는 주 평일과 비슷함
  
  ![img26](https://user-images.githubusercontent.com/83560273/147155806-c454261d-82e1-4139-a943-474e44941b37.JPG)
  
## 3. Modeling
- Metric
  
  ![img31](https://user-images.githubusercontent.com/83560273/147156733-21d954e4-ce76-4490-bada-0629c9193c58.JPG)

- Feature Selection
  - 쏘카 데이터
    - 대여일시, 반납일시 관련 파생변수(이용건수, 대여월, 대여주차, 대여요일, 대여건수, 공휴일 여부)  
    - 그룹별 사용량 관련 파생변수 : 성별/연령대별/차종별 요일 평균 사용량
  - 외부 데이터(날씨 변수)
    - 날씨 예보 : 강수확률, 기온, 습도, 풍속
    - 실제 관측 데이터 : 강수량, 미세먼지/초미세먼지, 일사량
  
  ![img32](https://user-images.githubusercontent.com/83560273/147156741-121d8c7c-ae36-48d0-9755-18d141fd8b77.JPG)
  
- Modeling
  - Linear Regression
  
  ![img33](https://user-images.githubusercontent.com/83560273/147156855-c4fc8b71-8fd1-434d-8677-ee192cf1b987.JPG)
  
  - XGBOOST + OPTUNA
  
  ![img34](https://user-images.githubusercontent.com/83560273/147156756-dd4b7d39-f0c5-487f-a356-2e117552006e.JPG)
  
- Validation
  - 평가결과(Score)
  
  ![img81](https://user-images.githubusercontent.com/83560273/147153836-ef96436d-3483-43e8-9698-78c7e3c61cde.JPG)

- Insight
  - 비가 내려도 이용시간이 증가하는 날이 있는 반면, 비가 내리지 않았는데 이용시간이 감소하는 날이 있음   
  - 날씨 변수 뿐만 아니라 여러 복합적인 요인들이 MIX되어 카셰어링 이용시간에 영향을 준다는 것을 알 수 있었음

  
## 4. 마케팅 포인트 제안
- 지역적 특성, 날씨, 공휴일 마케팅 관련 마케팅 포인트 도출
  - 비가 3일 이상 내린 경우
  
  ![img91](https://user-images.githubusercontent.com/83560273/147151499-fcc2aace-073a-4000-aef4-e4db7874929e.JPG)
  - 그 외 마케팅 포인트
  
  ![img92](https://user-images.githubusercontent.com/83560273/147151504-7696a03c-33a3-4f6a-9e1a-2c956ddf059b.JPG)

## 5. 프로젝트 회고
- 협업 관련
  - 코로나 19로 인한 사회적 거리두기 단계 지침으로 인해 프로젝트가 온라인으로 진행되면서 어려운 부분이 있었지만, 4인 이하 오프라인 모임 가능 시기와 화상회의, 슬랙/노션 등의 협업툴을 적시 적소에 활용하여 프로젝트를 성공적으로 마친 부분에 의의가 있다고 생각합니다.
  - 프로젝트 중 팀원이 변경되는 이슈가 있었음에도 짧은 시간 내에 적절한 업무 분배를 통해 외부데이터 수집, EDA 등 진행이 효율적으로 진행되었던 것 같습니다. 
  - 팀원들이 가지고 있는 개별 역량(모델링, 통계분석, 도메인 지식 등)이 모두 달랐기 때문에 각 팀원이 가지고 있는 역량 중심으로 업무 분배가 잘 되었던 것 같습니다.
- 데이터 관련
  - 매년 날씨의 특성은 다른데, 이용시간과 날씨의 관계를 비교해볼 수 있는 쏘카 데이터가 부족했던 점
  - d-0, d-1, d-2등 일자별 강수예보에 따른 쏘카 예약률 추이를 확인해볼 수 있는 데이터가 없었던 점
  - 이용량과 높은 상관관계가 있을 것이라 생각되었던 적설량 데이터가 충분하지 않아 분석을 못해본 점
