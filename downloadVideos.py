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
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        try:
            info = ydl.extract_info(URL, download=downloadVideo)
            print(json.dumps(ydl.sanitize_info(info)))
            with open(cid+'.json', 'w', encoding='utf8') as f:
                f.write(json.dumps(ydl.sanitize_info(info)))
         
        except Exception as e:  # skipcq: PYL-W0703
            print(e)


        

cid = get_cid_from_URL(URL)


print("start processing---\n",URL)    
if not os.path.exists(cid):
    print('prepare dir:',cid)
    os.mkdir(cid)
print("video download folder ---\n",'./'+cid)    

downloadvideosfromfreshchannel(URL,downloadVideo, './'+cid,Height,isSubtitle)
