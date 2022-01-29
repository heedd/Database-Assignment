# Database-Assignment
(2020년 3-1) 데이터베이스 과제

## 개발 환경
* 개발 환경 : Pycharm IDE (Project Interpreter : Python3.7), MariaDB 10.4.11 (phpMyAdmin)
* 사용 도구 : pymysql, pandas, matplotlib 라이브러리 사용
  
## 분석 주제
* 최근 5년 서울특별시 부동산 거래 현황 분석  

## 분석한 데이터
[(1) 서울특별시 부동산 실거래가 정보.csv](http://data.seoul.go.kr/dataList/OA-15548/S/1/datasetView.do)   
2016\~2020년 거래가 신고된 부동산의 관련 정보 660,000건  
[(2) 서울특별시 전월세가 정보.csv](http://data.seoul.go.kr/dataList/OA-15549/S/1/datasetView.do)  
2011\~2020년 사이 계약된 전월세 관련 정보 660,000건 
###### \* '서울 부동산 정보광장'이 제공한 데이터를 '서울 열린데이터 광장' 사이트에서 다운로드하여 사용  

## 프로그램 설명
* **데이터 load.py**    
\- 두 데이터를 전처리(결측치, 중복값 제거 등)한 후, MySQL서버와 연결하여 '(연도)\_자치구별_부동산_거래현황' 테이블을 create하는 쿼리 수행  

* **데이터 응용.py**  
\- MySQL서버의 테이블에 쿼리로 데이터를 조회하고, matplotlib로 데이터 분석 결과를 시각화
