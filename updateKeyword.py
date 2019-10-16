from config import apikey, host, user, password, db, charset
import requests
import json
import pymysql
import datetime

def searchKeyword(maxResults, q):
    #GET https://www.googleapis.com/youtube/v3/videos
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {'part': 'id,snippet', 'order': 'date', 'maxResults': maxResults, 'q': q, 'regionCode': 'KR', 'key': apikey, 'type': 'video', 'videoType': 'any'}
    result = requests.get(url=url, params=params)
    return result


def handler():
    con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset, autocommit=True)
    curs = con.cursor()

    sql = "SELECT DISTINCT hashtag FROM instar_register"
    sql2 = "INSERT INTO youtubeKeywordTotal (hashtag, total_num, register_Date) VALUES (%s, %s, %s)"
    curs.execute(sql)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = curs.fetchall()
    for row in rows:
        hashtag = row[0]
    
        datas = searchKeyword(5, hashtag)
        datas = json.loads(datas.text) #result to json
        totalResult = datas['pageInfo']['totalResults']
        print(hashtag, totalResult)

        curs.execute(sql2, (hashtag, totalResult, now))
    
    curs.close()
    con.close()

if __name__ == "__main__":
    handler()
