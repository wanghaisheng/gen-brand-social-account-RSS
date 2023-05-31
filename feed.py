from feedgen.feed import FeedGenerator

import json
import yt_dlp
import re
import os


URL = os.getenv('URL')
Height = os.getenv('downloadVideoHeight')
downloadVideo = os.getenv('downloadVideo')
isSubtitle=os.getenv('downloadSubtitles')
print('whether download video:',downloadVideo)


def get_cid_from_URL(URL):


    # regular channel url  pattern 
    # URL = 'https://youtube.com/channel/UCnDWguR8mE2oDBsjhQkgbvg'
    # URL = 'https://youtube.com/channel/UCBSQxFi6a8Ju2v_hgiM78Ew'
    # empty channel without any video uploaded 
    #'https://www.youtube.com/channel/UC7xBqZEJn3bgCf5GHkg95Iw/'
    # customized channel pattern 
    #'https://www.youtube.com/@KeywordsEverywhere/channels'
    if URL.startswith(('https://youtube.com/channel/', 'https://www.youtube.com/channel/','https://www.youtube.com/@')):
        print('valid url')
        if URL.startswith('https://youtube.com/channel/') or URL.startswith("https://www.youtube.com/channel/"):

            print('====',URL.split("https://youtube.com/channel/"))
            cid=URL.split("channel")[1]

            print("after replace---\n",cid)    

            # cid = 'UCBSQxFi6a8Ju2v_hgiM78Ew'
            if cid.endswith("/"):
                cid=cid.replace('/','')

        else:
            #https://www.youtube.com/@KeywordsEverywhere/channels
            print('====',URL.split("https://www.youtube.com/@"))
            cid=URL.split("@")[1]

            print("after replace---\n",cid)    
            cid=cid.split("/")[0]

            # cid = 'UCBSQxFi6a8Ju2v_hgiM78Ew'
            if cid.endswith("/"):
                cid=cid.replace('/','')       
            URL ="https://www.youtube.com/@"+cid            
        print("start processing---\n",URL)    
        return cid
    else:
        return None
def youtubechannelrssfromurl(URL):

    try:
        # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
        ydl_opts = {
            'verbose': True,

        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            try:
                info = ydl.extract_info(URL)
                channel_id=info['channel_id']

                return "https://www.youtube.com/feeds/videos.xml?channel_id="+channel_id

            except Exception as e:  # skipcq: PYL-W0703
                print(e)

                return None        
    except:
        print('invalid url')
def gen_Rss_from_url(URL):
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    print('your preferred is :',downloadVideo,Height)
    ydl_opts = {
        # 'proxy': 'socks5://127.0.0.1:1080'
        'verbose': True,

    }
    fg = FeedGenerator()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        try:
            info = ydl.extract_info(URL)
            print(json.dumps(ydl.sanitize_info(info)))
            with open(cid+'.json', 'w', encoding='utf8') as f:
                f.write(json.dumps(ydl.sanitize_info(info)))
            fg.load_extension('podcast')    
                
            fg.title(info['channel'])
            fg.link(href=info['uploader_url'])
            fg.description(info['uploader'])
            fg.podcast.itunes_author = info['uploader']
            fg.podcast.itunes_block = 'yes'
            fg.podcast.itunes_image = info['thumbnails'][0]['url']
            fg.podcast.itunes_explicit = 'no'
            fg.podcast.itunes_complete = None
            fg.podcast.itunes_new_feed_url = None
            fg.podcast.itunes_owner = None
            fg.podcast.itunes_subtitle = info['uploader']
            fg.podcast.itunes_summary = None
            fg.podcast.itunes_category(','.join(info['entries'][0]['categories']))
            # fg.podcast.channel_title(info['channel'])
            for idx,entry in enumerate(info['entries']):
                fe = fg.add_entry()
                fe.id(entry['id'])
                fe.title(entry['title'])
                fe.link(href=entry['webpage_url'])
                fe.description(entry['description'])
                fe.enclosure(yourowndomain+entry['id']+'.mp4', 0, 'video/mp4')

                fe.itunes_author = entry['uploader']
                fe.itunes_block = None
                fe.itunes_image = entry['thumbnail']
                fe.itunes_duration = entry['duration']
                fe.itunes_explicit = 'no'
            #     fe.itunes_is_closed_captioned = None
                fe.itunes_order = str(idx)
                fe.itunes_subtitle = entry['title']
                fe.itunes_summary = '<![CDATA[{}]]'.format(entry['description'])
                fe.itunes_season = None
                fe.itunes_episode = None
                fe.itunes_title = entry['fulltitle']
                fe.itunes_episode_type = None
            fg.rss_str(pretty=True)                
        except Exception as e:  # skipcq: PYL-W0703
            print(e)

            fg.title('xxxx')
            fg.link(href=URL)
            fg.description('xxxx')
        fg.rss_file(cid+'.xml')    
def downloadvideosfromfreshchannel(URL, downloadVideo,videodir,Height,isSubtitle:bool=False):
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    print('your preferred is :',downloadVideo,Height)
    ytp_format='bestvideo[height<={}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[height<={}][ext=mp4][vcodec^=avc1]/best[ext=mp4]/best'.format(Height,Height)
        
    ydl_opts = {
        'outtmpl': videodir+'/%(title).200B%(title.201B&…|)s.%(ext)s',
        'format': ytp_format,
        # 'proxy': 'socks5://127.0.0.1:1080'
        'writesubtitles': isSubtitle, 
        'writeautomaticsub': isSubtitle,
        'verbose': True,

    }
    fg = FeedGenerator()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        try:
            info = ydl.extract_info(URL, download=downloadVideo)
            print(json.dumps(ydl.sanitize_info(info)))
            with open(cid+'.json', 'w', encoding='utf8') as f:
                f.write(json.dumps(ydl.sanitize_info(info)))
            fg.load_extension('podcast')    
                
            fg.title(info['channel'])
            fg.link(href=info['uploader_url'])
            fg.description(info['uploader'])
            fg.podcast.itunes_author = info['uploader']
            fg.podcast.itunes_block = 'yes'
            fg.podcast.itunes_image = info['thumbnails'][0]['url']
            fg.podcast.itunes_explicit = 'no'
            fg.podcast.itunes_complete = None
            fg.podcast.itunes_new_feed_url = None
            fg.podcast.itunes_owner = None
            fg.podcast.itunes_subtitle = info['uploader']
            fg.podcast.itunes_summary = None
            fg.podcast.itunes_category(','.join(info['entries'][0]['categories']))
            # fg.podcast.channel_title(info['channel'])
            for idx,entry in enumerate(info['entries']):
                fe = fg.add_entry()
                fe.id(entry['id'])
                fe.title(entry['title'])
                fe.link(href=entry['webpage_url'])
                fe.description(entry['description'])
                fe.enclosure(yourowndomain+entry['id']+'.mp4', 0, 'video/mp4')

                fe.itunes_author = entry['uploader']
                fe.itunes_block = None
                fe.itunes_image = entry['thumbnail']
                fe.itunes_duration = entry['duration']
                fe.itunes_explicit = 'no'
            #     fe.itunes_is_closed_captioned = None
                fe.itunes_order = str(idx)
                fe.itunes_subtitle = entry['title']
                fe.itunes_summary = '<![CDATA[{}]]'.format(entry['description'])
                fe.itunes_season = None
                fe.itunes_episode = None
                fe.itunes_title = entry['fulltitle']
                fe.itunes_episode_type = None
            fg.rss_str(pretty=True)                
        except Exception as e:  # skipcq: PYL-W0703
            print(e)

            fg.title('xxxx')
            fg.link(href=URL)
            fg.description('xxxx')
        fg.rss_file(cid+'.xml')
        

cid = get_cid_from_URL(URL)
# after each video to podcast sync,we store local rss file to futher comparison
# filename would be platform_cid.xml or platform_cid.json
# if local rss file not exist we request a youtubechannelrssfromurl
# if youtubechannelrssfromurl failed ,we gen_Rss_from_url
gen_Rss_from_url(URL)        

# if local rss exist,we get remote rss using cid ,
# json =get(rssurl)

## compare two files to find differences

## download diff audio,thumbnail from video to later uploading 
# if a video contains no subtitles or subtiles file size low than xx kb, we consider it as a music video 

## publish to target platform

# regular channel url  pattern 
# URL = 'https://youtube.com/channel/UCnDWguR8mE2oDBsjhQkgbvg'
# URL = 'https://youtube.com/channel/UCBSQxFi6a8Ju2v_hgiM78Ew'
# empty channel without any video uploaded 
#'https://www.youtube.com/channel/UC7xBqZEJn3bgCf5GHkg95Iw/'
# customized channel pattern 
#'https://www.youtube.com/@KeywordsEverywhere/channels'
if URL.startswith(('https://youtube.com/channel/', 'https://www.youtube.com/channel/','https://www.youtube.com/@')):
    print('valid url')
    rssURL=youtubechannelrssfromurl(URL)
    if rssURL is None:
        
        if URL.startswith('https://youtube.com/channel/') or URL.startswith("https://www.youtube.com/channel/"):

            print('====',URL.split("https://youtube.com/channel/"))
            cid=URL.split("channel")[1]

            print("after replace---\n",cid)    

            # cid = 'UCBSQxFi6a8Ju2v_hgiM78Ew'
            if cid.endswith("/"):
                cid=cid.replace('/','')

        else:
            #https://www.youtube.com/@KeywordsEverywhere/channels
            print('====',URL.split("https://www.youtube.com/@"))
            cid=URL.split("@")[1]

            print("after replace---\n",cid)    
            cid=cid.split("/")[0]

            # cid = 'UCBSQxFi6a8Ju2v_hgiM78Ew'
            if cid.endswith("/"):
                cid=cid.replace('/','')       
            URL ="https://www.youtube.com/@"+cid            
        print("start processing---\n",URL)    
        if not os.path.exists(cid):
            print('prepare dir:',cid)
            os.mkdir(cid)
        downloadvideosfromfreshchannel(URL,downloadVideo, './'+cid,Height,isSubtitle)
    else:
        print('we can move on to next step',rssURL)
        
    ## detect rssurl content changes
    
    ## upload new episode to target platform
else:
    print('invalid url')
