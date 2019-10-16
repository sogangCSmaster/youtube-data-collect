from config import apikey, host, user, password, db, charset
import requests
import json
import pymysql
import datetime


def getStatistics(channelId):
    #GET https://www.googleapis.com/youtube/v3/channels
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {'part': 'statistics,snippet', 'id': channelId, 'key': apikey}
    result = requests.get(url=url, params=params)
    return result


def main():
    con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset, autocommit=True)
    curs = con.cursor()
    

    sql = "SELECT channelId FROM youtubeChannelList"
    curs.execute(sql)

    channelIds = curs.fetchall()

    for channelId in channelIds:
        try:
            channelId = channelId[0]

            result = getStatistics(channelId)
            result = json.loads(result.text)
            print(result)
            
            items = result['items'][0]
            statistics = items['statistics']
            viewCount = statistics['viewCount']
            commentCount = statistics['commentCount']
            subscriberCount = statistics['subscriberCount']
            videoCount = statistics['videoCount']

            now = datetime.datetime.now()
            updateTime = now.strftime('%Y-%m-%d %H:%M:%S')
            
            sql = "INSERT INTO youtubeChannelStatistics (channelId, updateTime, viewCount, commentCount, subscriberCount, videoCount) VALUES (%s, %s, %s, %s, %s, %s)"
            curs.execute(sql, (channelId, updateTime, viewCount, commentCount, subscriberCount, videoCount))
        except Exception as e:
            print(e)
    
    

    con.close()

if __name__ == "__main__":
    main()
    
