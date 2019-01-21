from config import apikey, host, user, password, db, charset
import requests
import json
import pymysql
import datetime
from categoryList import categoryList

def mostPopular(maxResults):
    #GET https://www.googleapis.com/youtube/v3/videos
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {'part': 'id,snippet,contentDetails,statistics,status,topicDetails', 'chart': 'mostPopular', 'maxResults': maxResults, 'regionCode': 'KR', 'key': apikey}
    result = requests.get(url=url, params=params)
    return result

def mostPopular_next(maxResults, nextPageToken):
    #GET https://www.googleapis.com/youtube/v3/videos
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {'part': 'id,snippet,contentDetails,statistics,status,topicDetails', 'chart': 'mostPopular', 'maxResults': maxResults, 'regionCode': 'KR', 'key': apikey, "pageToken": nextPageToken}
    result = requests.get(url=url, params=params)
    return result

def update_channel(channelId):
    #GET https://www.googleapis.com/youtube/v3/channels
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {'part': 'statistics,snippet,id,brandingSettings,topicDetails', 'id': channelId, 'key': apikey}
    result = requests.get(url=url, params=params)
    return result


def handler():
    con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset, autocommit=True)
    curs = con.cursor()
    
    channelIds = []
    
    datas = mostPopular(50)
    datas = json.loads(datas.text) #result to json
    print(datas)
    
    sql = "SELECT * FROM youtubeChannelList"
    curs.execute(sql)
    rows = curs.fetchall()
    print(rows)

    con.close()
    return "done"
