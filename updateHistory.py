from config import apikey, host, user, password, db, charset
import json
import pymysql
import datetime

def main():
    con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset, autocommit=True)
    curs = con.cursor()
    f = '%Y-%m-%d %H:%M:%S'
    

    sql = """
    SELECT 
	t.channelId,
	youtubeChannelList.title,
	MAX(updateTime) AS updateTime,
	(
		SELECT viewCount FROM youtubeChannelStatistics WHERE channelId = t.channelId ORDER BY updateTime DESC LIMIT 1
	) AS viewCount,
	(
		SELECT commentCount FROM youtubeChannelStatistics WHERE channelId = t.channelId ORDER BY updateTime DESC LIMIT 1
	) AS commentCount,
	(
		SELECT subscriberCount FROM youtubeChannelStatistics WHERE channelId = t.channelId ORDER BY updateTime DESC LIMIT 1
	) AS subscriberCount,
	(
		SELECT videoCount FROM youtubeChannelStatistics WHERE channelId = t.channelId ORDER BY updateTime DESC LIMIT 1
	) AS videoCount,
	(
		(SELECT viewCount FROM youtubeChannelStatistics WHERE channelId = t.channelId ORDER BY updateTime DESC LIMIT 1) -
		(SELECT viewCount from youtubeChannelStatistics t1 WHERE t1.updateTime < 
			(SELECT MAX(updateTime) FROM youtubeChannelStatistics WHERE channelId = t.channelId)
		AND t1.channelId = t.channelId order by updateTime DESC LIMIT 1)
	) AS viewDiff,
	(
		(SELECT commentCount FROM youtubeChannelStatistics WHERE channelId = t.channelId ORDER BY updateTime DESC LIMIT 1) -
		(SELECT commentCount from youtubeChannelStatistics t2 WHERE t2.updateTime < 
			(SELECT MAX(updateTime) FROM youtubeChannelStatistics WHERE channelId = t.channelId)
		AND t2.channelId = t.channelId order by updateTime DESC LIMIT 1)
	) AS commentDiff,
	(
		(SELECT subscriberCount FROM youtubeChannelStatistics WHERE channelId = t.channelId ORDER BY updateTime DESC LIMIT 1) -
		(SELECT subscriberCount from youtubeChannelStatistics t3 WHERE t3.updateTime < 
			(SELECT MAX(updateTime) FROM youtubeChannelStatistics WHERE channelId = t.channelId)
		AND t3.channelId = t.channelId order by updateTime DESC LIMIT 1)
	) AS subscriberDiff,
	(
		(SELECT videoCount FROM youtubeChannelStatistics WHERE channelId = t.channelId ORDER BY updateTime DESC LIMIT 1) -
		(SELECT videoCount from youtubeChannelStatistics t4 WHERE t4.updateTime < 
			(SELECT MAX(updateTime) FROM youtubeChannelStatistics WHERE channelId = t.channelId)
		AND t4.channelId = t.channelId order by updateTime DESC LIMIT 1)
	) AS videoDiff
    from youtubeChannelStatistics t JOIN youtubeChannelList ON t.channelId = youtubeChannelList.channelId GROUP BY t.channelId
    """
    curs.execute(sql)

    rows = curs.fetchall()

    for row in rows:
        channelId = row[0]
        title = row[1]
        updateTime = row[2]
        updateTime = updateTime.strftime(f)
        viewCount = row[3]
        commentCount = row[4]
        subscriberCount = row[5]
        videoCount = row[6]
        viewDiff = int(row[7])
        commentDiff = int(row[8])
        subscriberDiff = int(row[9])
        videoDiff = int(row[10])
        print(updateTime)
        option = (channelId, title, updateTime, viewCount, commentCount, subscriberCount, videoCount, viewDiff, commentDiff, subscriberDiff, videoDiff)

        sql = "INSERT INTO youtubeChannelHistory (channelId, title, updateTime, viewCount, commentCount, subscriberCount, videoCount, viewDiff, commentDiff, subscriberDiff, videoDiff) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, option)


    con.close()

if __name__ == "__main__":
    main()
    
