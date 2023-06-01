from feedgen.feed import FeedGenerator

import json
import yt_dlp
import re
import os


URL = os.getenv('URL')
Height = os.getenv('downloadVideoHeight')
isDownloadVideo = os.getenv('downloadVideo')
isSubtitle=os.getenv('downloadSubtitles')
isComments=os.getenv('downloadComments')
isAudioOnly=os.getenv('downloadOnlyAudio')


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
def downloadvideosfromfreshchannel(URL, isDownloadVideo,videodir,Height,isSubtitle:bool=False,isComments:bool=False,isAudioOnly:bool=False):
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    print('your preferred is :',isDownloadVideo,isSubtitle,isComments,isAudioOnly)


    if isAudioOnly:
        if not os.path.exists(videodir+'/'+'audio'):
        
            os.mkdir(videodir+'/'+'audio')

        ydl_opts = {
            'outtmpl': videodir+'/audio/'+'%(title).200B%(title.201B&…|)s.%(ext)s',
#             'extract_audio': True,
            'verbose': True,

            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        isDownloadVideo=True
    else:
        ytp_format='bestvideo[height<={}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[height<={}][ext=mp4][vcodec^=avc1]/best[ext=mp4]/best'.format(Height,Height)
        
        ydl_opts = {
            'outtmpl': videodir+'/'+'%(title).200B%(title.201B&…|)s.%(ext)s',
            'format': ytp_format,
            # 'proxy': 'socks5://127.0.0.1:1080'
            'verbose': True,

        }
        # python object to be appended
        y = {        
            'writesubtitles': isSubtitle, 
            'writeautomaticsub': isSubtitle,
            "subtitleslangs": ["all", "-live_chat"],        
            'getcomments': isComments,
            'writeinfojson': isComments,}


        ydl_opts =  ydl_opts | y
    print('whether download video:',isDownloadVideo)
    print('whether download subtitle:',isSubtitle)
    print('whether download comment:',isComments)
    print('whether download audio:',isAudioOnly)
    print('your ydl_opts is :',ydl_opts)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        try:
            info = ydl.extract_info(URL, download=isDownloadVideo)
#             print(json.dumps(ydl.sanitize_info(info)))
            with open(cid+'.json', 'w', encoding='utf8') as f:
                f.write(json.dumps(ydl.sanitize_info(info)))
         
        except Exception as e:  # skipcq: PYL-W0703
            print(e)


        

cid = get_cid_from_URL(URL)
if not os.path.exists('output'):
    os.mkdir('output')
if cid:

    print("start processing---\n",URL)    
    if not os.path.exists("./output/"+cid):
        print('prepare dir:',cid)
        os.mkdir("./output/"+cid)

    print("video download folder ---\n",'./'+cid)    

    downloadvideosfromfreshchannel(URL,isDownloadVideo, './output/'+cid,Height,isSubtitle,isComments,isAudioOnly)
else:
    print('please input a valid url',URL)
