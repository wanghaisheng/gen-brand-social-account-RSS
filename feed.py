from feedgen.feed import FeedGenerator

import json
import yt_dlp
import re
import os
# URL = 'https://youtube.com/channel/UCnDWguR8mE2oDBsjhQkgbvg'
# URL = 'https://youtube.com/channel/UCBSQxFi6a8Ju2v_hgiM78Ew'
URL = os.getenv('URL')
channeid=URL.replace('https://youtube.com/channel/','')
# channeid = 'UCBSQxFi6a8Ju2v_hgiM78Ew'
yourowndomain = 'https://distbit.loophole.site/'+channeid+'/'


def downloadvideosfromchannel(url, videodir):
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {
        'outtmpl': videodir+'/%(id)s'+'.mp4',
        'format': 'bestvideo[height<={}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[height<={}][ext=mp4][vcodec^=avc1]/best[ext=mp4]/best'.format(480,480),
        # 'proxy': 'socks5://127.0.0.1:1080'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=True)
#         with open(channeid+'.json', 'w', encoding='utf8') as f:
#             f.write(json.dumps(ydl.sanitize_info(info)))

        fg = FeedGenerator()
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
        fg.rss_file(channeid+'.xml')


if not os.path.exists(channeid):
    os.mkdir(channeid)
downloadvideosfromchannel(URL, './'+channeid)
