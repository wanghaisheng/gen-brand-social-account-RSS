from feedgen.feed import FeedGenerator

import json
import yt_dlp
import re
import os


URL = os.getenv('URL')


def url2rssURL(URL):
    if  "youtube.com" in URL:
        
        if URL.startswith('https://youtube.com/channel/') or URL.startswith("https://www.youtube.com/channel/"):

            channel_id=URL.split("channel/")[1]

            print("after replace---\n",channel_id)    

            # channel_id = 'UCBSQxFi6a8Ju2v_hgiM78Ew'
            if channel_id.endswith("/"):
                channel_id=channel_id.replace('/','')
            return "https://www.youtube.com/feeds/videos.xml?channel_id="+channel_id
        else:

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

                    print("start processing---\n",URL)    
                    if not os.path.exists(channel_id):
                        print('prepare dir:',channel_id)
                        os.mkdir(channel_id)
                    rssurl = genrssfromchannel(URL)
                    return rssurl        
    else:
        print('invalid url')
        return None
def channel_id2rssurl(channel_id):
    return "https://www.youtube.com/feeds/videos.xml?channel_id="+channel_id
def genrssfromchannel(url):
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    print('your preferred is :',downloadVideo,Height)
    ydl_opts = {
#         'outtmpl': videodir+'/%(title).200B%(title.201B&…|)s.%(ext)s',
#         'format': 'bestvideo[height<={}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[height<={}][ext=mp4][vcodec^=avc1]/best[ext=mp4]/best'.format(Height,Height),
        # 'proxy': 'socks5://127.0.0.1:1080'
        'verbose': True,

    }
    fg = FeedGenerator()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        try:
            info = ydl.extract_info(URL)
            print(json.dumps(ydl.sanitize_info(info)))
            with open(channel_id+'.json', 'w', encoding='utf8') as f:
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
        fg.rss_file(channel_id+'.xml')
        return channel_id+'.xml'
rssurl = url2rssURL(URL)
print('we found rss url is :',rssurl)
