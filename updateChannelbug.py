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

def mostPopular_next(maxResults, nextPageToken):
    #GET https://www.googleapis.com/youtube/v3/videos
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {'part': 'id,snippet,contentDetails,statistics,status,topicDetails', 'chart': 'mostPopular', 'maxResults': maxResults, 'regionCode': 'KR', 'key': apikey, "pageToken": nextPageToken}
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

    sql = "SELECT channelId FROM youtubeChannelList WHERE thumbnails=''"
    curs.execute(sql)
    channelIds = curs.fetchall()

    f = "%Y-%m-%dT%H:%M:%S.%fZ"

    for channelId in channelIds:
        result = update_channel(channelId[0])
        result = json.loads(result.text)

        items = result['items'][0]
        snippet = items['snippet']

        title = snippet['title']
        description = snippet['description']
        publishedAt = snippet['publishedAt']
        publishedAt = datetime.datetime.strptime(publishedAt, f)
        thumbnails = snippet['thumbnails']['default']['url']
        sql = "INSERT INTO youtubeChannelList (channelId, title, description, thumbnails, publishedAt) VALUES (%s, %s, %s, %s, %s)"

        try:
            curs.execute(sql, (channelId, title, description, thumbnails, publishedAt))
        except Exception as e:
            sql2 = "UPDATE youtubeChannelList SET thumbnails=%s WHERE channelId=%s"
            curs.execute(sql2, (thumbnails, channelId[0]))
    con.close()


if __name__ == "__main__":
    main()

