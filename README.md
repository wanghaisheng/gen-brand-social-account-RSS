# best tool to monitor brand social account posts is  RSS



## tiktok rss hub

https://github.com/feeddd/feeds



## 使用json存储
* 每一个videoid对应的channel id
* channel id对应的video list
* 对应的rss地址
  * youtube 频道rss是现成的
  * youtube trending也是现成的
  * youtube 关键词搜索？？  
* 
https://www.owenyoung.com/blog/jsonbin/

## supported sites

* youtube 
* tiktok 
* douyin 
* kuaishou

## monitor channel video changes 

youtube feed give us 15 entry in the feed xml,if check duration is longer,we may miss the new video


### get rss url from youtube  url 

https://github.com/wanghaisheng/turn-youtube-channel-to-podcast-rss/blob/main/youtuberss.py

get rss url like this. then you can monitor this url to get changes

https://www.youtube.com/feeds/videos.xml?channel_id=UC7_gcs09iThXybpVgjHZ_7g


### get rss url from douyin 


### get rss url from tiktok 



### for those urls can not get rss url, we can manually make one 

https://github.com/wanghaisheng/turn-youtube-channel-to-podcast-rss/blob/main/feed.py


### feed diff 

https://github.com/NicolasLM/atoma



## monitor video contents 


## download video and subtitle ,comments  from url 

comment analysis is important 

transcript keywords is important 


## download  audio only from url

for transcription extract, audio is more appopriate than video,less sapce,less processing time


https://user-images.githubusercontent.com/2363295/170819288-fa90b35d-f3b5-4c5c-9f17-4cdc80a680ac.mp4


## download thumbnail only from url

https://www.youtube.com/user/bgfilms/videos




## thanks 

https://github.com/open-tiktoka/tiktok-rss-gui/tree/main

https://github.com/Russell-Newton/TikTokPy

https://rss.app/rss-feed/tiktok-to-rss
