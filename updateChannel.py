from config import apikey, host, user, password, db, charset
import requests
import json
import pymysql
import datetime


def mostPopular(maxResults):
    #GET https://www.googleapis.com/youtube/v3/videos
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {'part': 'id,snippet,contentDetails,statistics,status,topicDetails', 'chart': 'mostPopular', 'maxResults': maxResults, 'regionCode': 'KR', 'key': apikey}
    result = requests.get(url=url, params=params)
    return result

def update_channel(channelId):
    #GET https://www.googleapis.com/youtube/v3/channels
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {'part': 'statistics,snippet', 'id': channelId, 'key': apikey}
    result = requests.get(url=url, params=params)
    return result


def main():
    con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset, autocommit=True)
    curs = con.cursor()
    
    channelIds = []
    
    datas = mostPopular(50)
    datas = json.loads(datas.text) #result to json
    items2 = datas['items']

    for item in items2:
        snippet = item['snippet']
        channelId = snippet['channelId']
        channelIds.append(channelId)

    f = "%Y-%m-%dT%H:%M:%S.%fZ"

    for channelId in channelIds:
        result = update_channel(channelId)
        result = json.loads(result.text)

        items = result['items'][0]
        snippet = items['snippet']

        title = snippet['title']
        description = snippet['description']
        publishedAt = snippet['publishedAt']
        publishedAt = datetime.datetime.strptime(publishedAt, f)
        thumbnails = ""
        sql = "INSERT INTO youtubeChannelList (channelId, title, description, thumbnails, publishedAt) VALUES (%s, %s, %s, %s, %s)"

        try:
            curs.execute(sql, (channelId, title, description, thumbnails, publishedAt))
        except Exception as e:
            sql2 = "UPDATE youtubeChannelList SET title=%s, description=%s, thumbnails=%s"
            curs.execute(sql2, (title, description, thumbnails))

    con.close()

if __name__ == "__main__":
    main()
    