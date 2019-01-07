from config import apikey, host, user, password, db, charset
import requests
import json
import pymysql
import datetime
import sys
import logging


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

    categoryList = ["1", "2", "10", "15", "17", "20", "23", "24", "26", "28"]
    

    
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

    
    result = mostPopular(50) 
    result = json.loads(result.text) #result to json
    items = result['items']

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

    
        if 'maxres' in snippet['thumbnails']:
            thumbnails = snippet['thumbnails']['maxres']['url']
        elif 'standard' in snippet['thumbnails']:
            thumbnails = snippet['thumbnails']['standard']['url']
        elif 'high' in snippet['thumbnails']:
            thumbnails = snippet['thumbnails']['high']['url']
        elif 'medium' in snippet['thumbnails']:
            thumbnails = snippet['thumbnails']['medium']['url']
        else:
            thumbnails = snippet['thumbnails']['default']['url']
        


        channelTitle = snippet['channelTitle']
        try:
            tags = snippet['tags']
        except:
            tags = []
        tags = json.dumps(tags, ensure_ascii=False)
        

        categoryId = snippet['categoryId']
        statistics = item['statistics']

        viewCount = None
        likeCount = None
        dislikeCount = None
        favoriteCount = None
        commentCount = None

        if 'viewCount' in statistics:
            viewCount = statistics['viewCount']
        if 'likeCount' in statistics:
            likeCount = statistics['likeCount']
        if 'dislikeCount' in statistics:
            dislikeCount = statistics['dislikeCount']
        if 'favoriteCount' in statistics:
            favoriteCount = statistics['favoriteCount']
        if 'commentCount' in statistics:
            commentCount = statistics['commentCount']


        if 'topicDetails' in item:
            topicDetails = item['topicDetails']
            try:
                topicCategories = topicDetails['topicCategories']
            except:
                topicCategories = []
        
        topicCategories = json.dumps(topicCategories, ensure_ascii=False)
        
        options = (timeId, ranking, reversedTimeId, videoId, publishedAt, channelId, channelTitle, title, description, thumbnails, categoryId, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, tags, topicCategories)
        sql = "INSERT INTO youtubeMostPopular (timeId, ranking, reversedTimeId, videoId, publishedAt, channelId, channelTitle, title, description, thumbnails, categoryId, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, tags, topicCategories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, options)



    for category in categoryList:
        result = mostPopular_category(50, category)
        result = json.loads(result.text)
        if 'items' in result:
            items = result['items']
            
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

            
                if 'maxres' in snippet['thumbnails']:
                    thumbnails = snippet['thumbnails']['maxres']['url']
                elif 'standard' in snippet['thumbnails']:
                    thumbnails = snippet['thumbnails']['standard']['url']
                elif 'high' in snippet['thumbnails']:
                    thumbnails = snippet['thumbnails']['high']['url']
                elif 'medium' in snippet['thumbnails']:
                    thumbnails = snippet['thumbnails']['medium']['url']
                else:
                    thumbnails = snippet['thumbnails']['default']['url']
                


                channelTitle = snippet['channelTitle']
                try:
                    tags = snippet['tags']
                except:
                    tags = []
                tags = json.dumps(tags, ensure_ascii=False)
                

                categoryId = snippet['categoryId']
                statistics = item['statistics']

                viewCount = None
                likeCount = None
                dislikeCount = None
                favoriteCount = None
                commentCount = None

                if 'viewCount' in statistics:
                    viewCount = statistics['viewCount']
                if 'likeCount' in statistics:
                    likeCount = statistics['likeCount']
                if 'dislikeCount' in statistics:
                    dislikeCount = statistics['dislikeCount']
                if 'favoriteCount' in statistics:
                    favoriteCount = statistics['favoriteCount']
                if 'commentCount' in statistics:
                    commentCount = statistics['commentCount']


                if 'topicDetails' in item:
                    topicDetails = item['topicDetails']
                    try:
                        topicCategories = topicDetails['topicCategories']
                    except:
                        topicCategories = []
                
                topicCategories = json.dumps(topicCategories, ensure_ascii=False)
                
                options = (timeId, ranking, reversedTimeId, videoId, publishedAt, channelId, channelTitle, title, description, thumbnails, categoryId, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, tags, topicCategories)
                sql = "INSERT INTO youtubePopular"+ category +" (timeId, ranking, reversedTimeId, videoId, publishedAt, channelId, channelTitle, title, description, thumbnails, categoryId, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, tags, topicCategories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                
                curs.execute(sql, options)

            
            
    con.close()


if __name__ == "__main__":
    main()

