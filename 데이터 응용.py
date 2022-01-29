import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
plt.rcParams['font.family'] = 'Malgun Gothic'

# MySQL Connection 연결
conn = pymysql.connect(
    user='root',
    passwd='',
    host='127.0.0.1',
    db='real_estate',
    charset='utf8'
)
curs = conn.cursor()
curd = conn.cursor(pymysql.cursors.DictCursor)


#서울특별시_매매, 서울특별시_전월세 테이블 조회
print("1. 2016년 가장 비싸게 매매된 건물을 검색하라")
sql = "SELECT  자치구명, 법정동명, 건물명, 물건금액 FROM 서울특별시_매매 " \
      "WHERE 신고년도=2016 AND 물건금액=(SELECT MAX(물건금액))"
curs.execute(sql); rows=curs.fetchone(); print(rows)

print("\n2. 2020년 서대문구에서 매매된 건축년도가 2015년 이후인 모든 건물명을 검색하라")
sql = "SELECT DISTINCT 건물명 FROM 서울특별시_매매 " \
      "WHERE 신고년도=2020 AND 자치구명='서대문구' AND 건축년도>=2015"
curd.execute(sql); print(pd.DataFrame(curd))

print("\n3. 2020년 서초구 반포동에서 매매된 아파트 수를 검색하라",end='\n')
sql = "SELECT count(*) as 매매량 FROM 서울특별시_매매  " \
      "WHERE 자치구명='서초구' AND 법정동명='반포동' AND 건물주용도='아파트' AND 신고년도=2020"
curs.execute(sql); rows=curs.fetchone(); print(rows)


print("\n4. 임대면적이 100~125m^2 이고, 보증금이 50000이하인 청담동 아파트 전세 거래기록을 검색하라")
sql = "SELECT * FROM 서울특별시_전월세 " \
      "WHERE 보증금<=50000 and 임대면적 between 100 and 125 and 전월세구분='전세' and 법정동명='청담동' and 임대건물명='아파트'"
curd.execute(sql); print(pd.DataFrame(curd))
for row in rows: print(row)

print("\n5. 2020년 부동산 전월세 계약 신고 건수가 많은 순서대로 양천구의 법정동명과 거래 건수를 검색하라")
sql = "SELECT 법정동명, COUNT(*) as 거래량 FROM 서울특별시_전월세 " \
      "WHERE 자치구명='양천구' " \
      "GROUP BY 법정동명 ORDER BY COUNT(*) DESC"
curd.execute(sql); df=pd.DataFrame(curd); print(df)
plt.title("양천구 법정동별 부동산 거래량", fontsize=18)
plt.xlabel('법정동명', fontsize=13); plt.ylabel('거래량', fontsize=13)
plt.ylim(0000,20000)
plt.bar(df['법정동명'], df['거래량'], width=0.5, color='g')
plt.show()

#지역구별 부동산거래 현황 테이블 조회
print("\n6. 연도별 부동산 총 거래량이 가장 많은 상위 5개 지역구를 검색하라")
for i in range(2016,2021):
    sql = "SELECT 자치구명, 총거래 from %s자치구별_부동산_거래현황 ORDER BY 총거래 DESC LIMIT 5"%i
    curd.execute(sql); df=pd.DataFrame(curd); print(i); print(df)

print("\n7. 연도, 지역구별 평균 거래가가 가장 높은 상위 5개 지역구를 검색하라")
for i in range(2016,2021):
    sql = "SELECT 자치구명, 평균실거래가 from %s자치구별_부동산_거래현황 ORDER BY 평균실거래가 asc LIMIT 5"%i
    curd.execute(sql); df=pd.DataFrame(curd); print(i); print(df)

print("\n8. 연도, 지역구별 평균 거래가의 추이를 검색하라")
for i in range(2016,2021):
    sql = "SELECT 자치구명, 평균실거래가 from %s자치구별_부동산_거래현황 ORDER BY 평균실거래가"%i
    curd.execute(sql); df=pd.DataFrame(curd); print(i); print(df)
    df['연도']=i

print("\n9. 연도, 지역구별 거래량의 추이를 검색하라")
for i in range(2016,2021):
    sql = "SELECT 자치구명, 총거래 from %s자치구별_부동산_거래현황 ORDER BY 총거래"%i
    curd.execute(sql); df=pd.DataFrame(curd); print(i); print(df)
    df['연도']=i

print("\n10. 2017년 대비 2020년 집값 상승폭이 큰 지역을 순서대로 검색하라")
sql = """SELECT e.자치구명, (e.평균실거래가-t.평균실거래가) as 증가금액, (e.평균실거래가/t.평균실거래가) as 상승율
    from 2020자치구별_부동산_거래현황 as e, 2017자치구별_부동산_거래현황 as t
    where e.자치구명=t.자치구명
    order by (e.평균실거래가 - t.평균실거래가) desc"""
curd.execute(sql); df=pd.DataFrame(curd); print(df)
plt.title("2017년 대비 2020년 지역구별 부동산 거래가 상승폭", fontsize=18)
plt.xlabel('자치구명', fontsize=13); plt.ylabel('증가금액', fontsize=13)
plt.bar(df['자치구명'], df['증가금액'], width=0.5, color='r')
plt.show()

conn.commit()
conn.close()
