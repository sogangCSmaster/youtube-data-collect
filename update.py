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
    params = {'part': 'id,snippet,contentDetails,statistics,status,topicDetails', 'chart': 'mostPopular', 'maxResults': maxResults, 'regionCode': 'KR', 'key': apikey, 'pageToken': nextPageToken}
    result = requests.get(url=url, params=params)
    return result

def mostPopular_category(maxResults, videoCategoryId):
    #GET https://www.googleapis.com/youtube/v3/videos
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {'part': 'id,snippet,contentDetails,statistics,status,topicDetails', 'chart': 'mostPopular', 'maxResults': maxResults, 'regionCode': 'KR', 'key': apikey, 'videoCategoryId': videoCategoryId}
    result = requests.get(url=url, params=params)
    return result

def main():
    con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset, autocommit=True)
    curs = con.cursor()
    
    result = mostPopular(50) 
    result = json.loads(result.text) #result to json

    items = result['items']
    sql = "SELECT max(timeId) as timeId FROM youtubeTimeline"
    curs.execute(sql)
    timeId = curs.fetchall()[0][0]
    timeId += 1
    reversedTimeId = timeId * -1
    
    
    now = datetime.datetime.now()
    updateTime = now.strftime('%Y-%m-%d %H:%M:%S')
    

    sql = "INSERT INTO youtubeTimeline (timeId, updateTime) VALUES (%s, %s)"
    curs.execute(sql, (timeId, updateTime))
    f = "%Y-%m-%dT%H:%M:%S.%fZ"

    
    for idx, item in enumerate(items):
        tags = []
        topicCategories = []

        ranking = idx + 1
        videoId = item['id']
        snippet = item['snippet']
        publishedAt = snippet['publishedAt']
        publishedAt = datetime.datetime.strptime(publishedAt, f)
        channelId = snippet['channelId']
        title = snippet['title']
        description = snippet['description']
        try:
            thumbnails = snippet['thumbnails']['maxres']['url']
        except:
            thumbnails = snippet['thumbnails']['standard']['url']
        
        channelTitle = snippet['channelTitle']
        try:
            tags = snippet['tags']
        except:
            tags = []
        tags = json.dumps(tags, ensure_ascii=False)
        
        categoryId = snippet['categoryId']
        statistics = item['statistics']
        viewCount = statistics['viewCount']
        likeCount = statistics['likeCount']
        dislikeCount = statistics['dislikeCount']
        favoriteCount = statistics['favoriteCount']
        commentCount = statistics['commentCount']
        if item['topicDetails']:
            topicDetails = item['topicDetails']
            try:
                topicCategories = topicDetails['topicCategories']
            except:
                topicCategories = []
        
        topicCategories = json.dumps(topicCategories, ensure_ascii=False)
        
        options = (timeId, ranking, reversedTimeId, videoId, publishedAt, channelId, channelTitle, title, description, thumbnails, categoryId, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, tags, topicCategories)
        sql = "INSERT INTO youtubeMostPopular (timeId, ranking, reversedTimeId, videoId, publishedAt, channelId, channelTitle, title, description, thumbnails, categoryId, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, tags, topicCategories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, options)
    
    
    con.close()


if __name__ == "__main__":
    main()

