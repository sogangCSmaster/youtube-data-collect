# youtube-data-collect
collect youtube data to mysql for trending analysis

## youtubeCategory Table
- 유튜브 카테고리를 담아두는 테이블
### SQL
```
CREATE TABLE `youtubeCategory` (
  `categoryId` int(3) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  KEY `categoryId` (`categoryId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## youtubeMostPopular Table
- 유튜브 시간 별 랭킹 및 기타 정보를 담아두는 테이블
### SQL
```
CREATE TABLE `youtubeMostPopular` (
  `timeId` int(11) DEFAULT NULL,
  `ranking` int(5) DEFAULT NULL,
  `reversedTimeId` int(11) DEFAULT NULL,
  `videoId` varchar(50) DEFAULT NULL,
  `publishedAt` datetime DEFAULT NULL,
  `channelId` varchar(255) DEFAULT NULL,
  `channelTitle` varchar(255) DEFAULT NULL,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `thumbnails` varchar(255) DEFAULT NULL,
  `categoryId` int(3) DEFAULT NULL,
  `viewCount` int(11) DEFAULT NULL,
  `likeCount` int(11) DEFAULT NULL,
  `dislikeCount` int(11) DEFAULT NULL,
  `favoriteCount` int(11) DEFAULT NULL,
  `commentCount` int(11) DEFAULT NULL,
  `tags` text DEFAULT NULL,
  `topicCategories` text DEFAULT NULL,
  KEY `timeId` (`timeId`),
  KEY `reversedtimeId` (`reversedTimeId`),
  KEY `videoId` (`videoId`),
  KEY `channelID` (`channelId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## youtubeTimeline Table
- Update 시간을 저장할 테이블 - youtubeMostPopular 테이블의 timeId와 매치
### SQL
```
CREATE TABLE `youtubeTimeline` (
  `timeId` int(11) DEFAULT NULL,
  `updateTime` datetime DEFAULT NULL,
  KEY `timeId` (`timeId`),
  KEY `updateTime` (`updateTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```