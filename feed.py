from feedgen.feed import FeedGenerator

import json
import yt_dlp
import re
import os



URL = os.getenv('URL')
Height = os.getenv('downloadVideoHeight')
downloadVideo = os.getenv('downloadVideo')



def downloadvideosfromchannel(url, downloadVideo,videodir,Height):
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    print('your preferred is :',downloadVideo,Height)
    ydl_opts = {
        'outtmpl': videodir+'/%(alt_title,title){100B-excesslength}\%(title).100B [%(extractor)s.%(id)s] {%(format_id)s}.%(ext)s',
        'format': 'bestvideo[height<={}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[height<={}][ext=mp4][vcodec^=avc1]/best[ext=mp4]/best'.format(Height,Height),
        # 'proxy': 'socks5://127.0.0.1:1080'
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
        
# regular channel url  pattern 
# URL = 'https://youtube.com/channel/UCnDWguR8mE2oDBsjhQkgbvg'
# URL = 'https://youtube.com/channel/UCBSQxFi6a8Ju2v_hgiM78Ew'
# empty channel without any video uploaded 
#'https://www.youtube.com/channel/UC7xBqZEJn3bgCf5GHkg95Iw/'
# customized channel pattern 
#'https://www.youtube.com/@KeywordsEverywhere/channels'
if URL.startswith(('https://youtube.com/channel/', 'https://www.youtube.com/@')):
    print('valid url')
    if URL.startswith('https://youtube.com/channel/'):
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
    downloadvideosfromchannel(URL,downloadVideo, './'+cid,Height)
    
else:
    print('invalid url')
