import pandas as pd
import pymysql
import os

#데이터 불러오기
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
df1=pd.read_csv(r'C:/Users/clari/Desktop/db2/서울특별시 부동산 실거래가 정보1.csv', encoding='utf-8')
df1=df1.drop(['지번코드','업무구분','시군구코드','법정동코드','업무구분코드','물건번호','관리구분코드','건물주용도코드'], axis=1)
df1=df1.fillna(0); df1=df1.drop_duplicates(keep='first')

df2=pd.read_csv(r'C:/Users/clari/Desktop/db2/서울특별시 전월세가 정보1.csv', encoding='utf-8')
df2=df2.drop(['지번코드','자치구코드','법정동코드','본번','부번','임대건물코드','전월세구분코드'], axis=1)
df2=df2.fillna(0); df2=df2.drop_duplcates(keep='first')
arr=[]
for i in range(len(df2)):
    arr.append(i)
df3=pd.DataFrame({"거래아이디":arr})
df2=pd.concat([df3,df2], axis=1)

# MySQL Connection 연결
conn = pymysql.connect(
    user='root',
    passwd='',
    host='127.0.0.1',
    db='real_estate',
    charset='utf8'
)
curs = conn.cursor(pymysql.cursors.DictCursor)

#df1 전체를 서울특별시_매매 테이블에 insert
vals1 = tuple([tuple(x) for x in df1.values])
sql1 = "INSERT IGNORE INTO 서울특별시_매매 (실거래가아이디, 자치구명, 법정동명, 신고년도, 대지권면적\
                                   ,건물면적, 층정보, 건물주용도, 물건금액, 건물명, 건축년도)\
                                     VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
curs.executemany(sql1,vals1)
conn.commit()
print(curs.rowcount, "records were inserted in real_estate.서울특별시_매매")

#df2 전체를 서울특별시_전월세 테이블에 insert
vals2 = tuple([tuple(x) for x in df2.values])
sql2 = "INSERT IGNORE INTO 서울특별시_전월세 (거래아이디, 기관코드, 일련번호, 접수년도, 자치구명, 법정동명, 건물명, 층, 임대건물명, 임대면적,\
                                    전월세구분, 보증금, 임대료, 계약년도, 계약일자, 건축년도)\
                                     VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
curs.executemany(sql2, vals2)
conn.commit()
print(curs.rowcount, "records were inserted in real_estate.서울특별시_전월세")

sql="""create table 2020_자치구별_부동산_거래현황"\
		as
		select t1.자치구명, 매매, 전세, 준전세, 월세, 준월세, 총거래, 평균실거래가
		from
		((select 자치구명, count(전월세구분) as 전세 from 서울특별시_전월세 where 계약년도=2020 AND 전월세구분='전세' group by 자치구명) t1
		join (select 자치구명, count(전월세구분) as 준전세 from 서울특별시_전월세 where 계약년도=2020 AND 전월세구분='준전세' group by 자치구명) t2
		join (select 자치구명, count(전월세구분) as 월세 from 서울특별시_전월세 where 계약년도=2020 AND 전월세구분='월세' group by 자치구명) t3
		join (select 자치구명, count(전월세구분) as 준월세 from 서울특별시_전월세 where 계약년도=2020 AND 전월세구분='준월세' group by 자치구명) t4
		join (select 자치구명, count(전월세구분) as 총거래 from 서울특별시_전월세 where 계약년도=2020 group by 자치구명) t5
   		join (select 자치구명, count(자치구명) as 매매 from 서울특별시_매매 where 신고년도=2020 group by 자치구명) t6
   		join (select 자치구명, avg(물건금액) as 평균실거래가 from 서울특별시_매매 where 신고년도=2020 group by 자치구명) t7
		on t1.자치구명=t2.자치구명 and t2.자치구명=t3.자치구명 and t3.자치구명=t4.자치구명 and t4.자치구명=t5.자치구명
   		and t5.자치구명=t6.자치구명 and t6.자치구명=t7.자치구명 )"""
sql="create table 2019_자치구별_부동산_거래현황"\
"as"\
"select t1.자치구명, 매매, 전세, 준전세, 월세, 준월세, 총거래, 평균실거래가"\
"from"\
	"((select 자치구명, count(전월세구분) as 전세 from 서울특별시_전월세 where 계약년도=2019 AND 전월세구분='전세' group by 자치구명) t1"\
	"join"\
	"(select 자치구명, count(전월세구분) as 준전세 from 서울특별시_전월세 where 계약년도=2019 AND 전월세구분='준전세' group by 자치구명) t2"\
	"join"\
	"(select 자치구명, count(전월세구분) as 월세 from 서울특별시_전월세 where 계약년도=2019 AND 전월세구분='월세' group by 자치구명) t3"\
	"join"\
	"(select 자치구명, count(전월세구분) as 준월세 from 서울특별시_전월세 where 계약년도=2019 AND 전월세구분='준월세' group by 자치구명) t4"\
	"join"\
	"(select 자치구명, count(전월세구분) as 총거래 from 서울특별시_전월세 where 계약년도=2019 group by 자치구명) t5"\
    "join"\
	"(select 자치구명, count(자치구명) as 매매 from 서울특별시_매매 where 신고년도=2019 group by 자치구명) t6"\
    "join"\
	"(select 자치구명, avg(물건금액) as 평균실거래가 from 서울특별시_매매 where 신고년도=2019 group by 자치구명) t7"\
	"on t1.자치구명=t2.자치구명 and t2.자치구명=t3.자치구명 and t3.자치구명=t4.자치구명 and t4.자치구명=t5.자치구명 and t5.자치구명=t6.자치구명 and t6.자치구명=t7.자치구명 )";
sql="create table 2018_자치구별_부동산_거래현황"\
"as"\
"select t1.자치구명, 매매, 전세, 준전세, 월세, 준월세, 총거래, 평균실거래가"\
"from"\
	"((select 자치구명, count(전월세구분) as 전세 from 서울특별시_전월세 where 계약년도=2018 AND 전월세구분='전세' group by 자치구명) t1"\
	"join"\
	"(select 자치구명, count(전월세구분) as 준전세 from 서울특별시_전월세 where 계약년도=2018 AND 전월세구분='준전세' group by 자치구명) t2"\
	"join"\
	"(select 자치구명, count(전월세구분) as 월세 from 서울특별시_전월세 where 계약년도=2018 AND 전월세구분='월세' group by 자치구명) t3"\
	"join"\
	"(select 자치구명, count(전월세구분) as 준월세 from 서울특별시_전월세 where 계약년도=2018 AND 전월세구분='준월세' group by 자치구명) t4"\
	"join"\
	"(select 자치구명, count(전월세구분) as 총거래 from 서울특별시_전월세 where 계약년도=2018 group by 자치구명) t5"\
    "join"\
	"(select 자치구명, count(자치구명) as 매매 from 서울특별시_매매 where 신고년도=2018 group by 자치구명) t6"\
    "join"\
	"(select 자치구명, avg(물건금액) as 평균실거래가 from 서울특별시_매매 where 신고년도=2018 group by 자치구명) t7"\
	"on t1.자치구명=t2.자치구명 and t2.자치구명=t3.자치구명 and t3.자치구명=t4.자치구명 and t4.자치구명=t5.자치구명 and t5.자치구명=t6.자치구명 and t6.자치구명=t7.자치구명 )";
sql="create table 2017_자치구별_부동산_거래현황"\
"as"\
"select t1.자치구명, 매매, 전세, 준전세, 월세, 준월세, 총거래, 평균실거래가"\
"from"\
	"((select 자치구명, count(전월세구분) as 전세 from 서울특별시_전월세 where 계약년도=2017 AND 전월세구분='전세' group by 자치구명) t1"\
	"join"\
	"(select 자치구명, count(전월세구분) as 준전세 from 서울특별시_전월세 where 계약년도=2017 AND 전월세구분='준전세' group by 자치구명) t2"\
	"join"\
	"(select 자치구명, count(전월세구분) as 월세 from 서울특별시_전월세 where 계약년도=2017 AND 전월세구분='월세' group by 자치구명) t3"\
	"join"\
	"(select 자치구명, count(전월세구분) as 준월세 from 서울특별시_전월세 where 계약년도=2017 AND 전월세구분='준월세' group by 자치구명) t4"\
	"join"\
	"(select 자치구명, count(전월세구분) as 총거래 from 서울특별시_전월세 where 계약년도=2017 group by 자치구명) t5"\
    "join"\
	"(select 자치구명, count(자치구명) as 매매 from 서울특별시_매매 where 신고년도=2017 group by 자치구명) t6"\
    "join"\
	"(select 자치구명, avg(물건금액) as 평균실거래가 from 서울특별시_매매 where 신고년도=2017 group by 자치구명) t7"\
	"on t1.자치구명=t2.자치구명 and t2.자치구명=t3.자치구명 and t3.자치구명=t4.자치구명 and t4.자치구명=t5.자치구명 and t5.자치구명=t6.자치구명 and t6.자치구명=t7.자치구명 )";
sql="create table 2016_자치구별_부동산_거래현황"\
"as"\
"select t1.자치구명, 매매, 전세, 준전세, 월세, 준월세, 총거래, 평균실거래가"\
"from"\
	"((select 자치구명, count(전월세구분) as 전세 from 서울특별시_전월세 where 계약년도=2016 AND 전월세구분='전세' group by 자치구명) t1"\
	"join"\
	"(select 자치구명, count(전월세구분) as 준전세 from 서울특별시_전월세 where 계약년도=2016 AND 전월세구분='준전세' group by 자치구명) t2"\
	"join"\
	"(select 자치구명, count(전월세구분) as 월세 from 서울특별시_전월세 where 계약년도=2016 AND 전월세구분='월세' group by 자치구명) t3"\
	"join"\
	"(select 자치구명, count(전월세구분) as 준월세 from 서울특별시_전월세 where 계약년도=2016 AND 전월세구분='준월세' group by 자치구명) t4"\
	"join"\
	"(select 자치구명, count(전월세구분) as 총거래 from 서울특별시_전월세 where 계약년도=2016 group by 자치구명) t5"\
    "join"\
	"(select 자치구명, count(자치구명) as 매매 from 서울특별시_매매 where 신고년도=2016 group by 자치구명) t6"\
    "join"\
	"(select 자치구명, avg(물건금액) as 평균실거래가 from 서울특별시_매매 where 신고년도=2016 group by 자치구명) t7"\
	"on t1.자치구명=t2.자치구명 and t2.자치구명=t3.자치구명 and t3.자치구명=t4.자치구명 and t4.자치구명=t5.자치구명 and t5.자치구명=t6.자치구명 and t6.자치구명=t7.자치구명 )"
curs.execute(sql)
conn.commit()

#Connection 닫기
conn.close()

