from feedgen.feed import FeedGenerator

import json
import yt_dlp
import re
import os
import pandas

URL = os.getenv('URL')
Keywords = os.getenv('Keywords')
if ',' in Keywords:
    Keywords=Keywords.split(",")
else:
    Keywords=[Keywords]
url_cid_mapping_list=[]        
def remove_special_elements(lst):
    special_chars = "!@#$%^&*()-_=+[]{}|:;,.<>/?'\""

    lst= [elem for elem in lst if not all(char in special_chars for char in elem) or not elem.isalpha()]

    # return [elem.strip(''.join(list(special_chars))) for elem in lst]
    return lst
if os.path.exists("youtube-url-cid-mappings.csv")==False:
    
    with open("youtube-url-cid-mappings.csv", "w") as file:
        file.write("url,cid"+"\n")
else:
    if not os.stat("youtube-url-cid-mappings.csv").st_size == 0:
        url_cid_mapping_list = pandas.read_csv('youtube-url-cid-mappings.csv')


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
def keywords2RssURL(queries,feedname):
    # Starting the list where we will store the collected data:
    results = []
    
    fg = FeedGenerator()
    with yt_dlp.YoutubeDL() as ydl:

        try:
            # Collecting data for each query:
            description=None
            search_base='https://www.youtube.com/results?search_query='
            # https://www.youtube.com/results?search_query=hammersmith+infant+neurological+examination+(hine)       
            
            for idx,query in enumerate(queries):
                r = ydl.extract_info("ytsearchdateall:{}".format(query), download=False)
                results += r['entries']    
                description =search_base+query.replace(' ',"+")+'\n\r'
            with open(feedname+'.json', 'w', encoding='utf8') as f:
                f.write(json.dumps(ydl.sanitize_info(results)))
            print('1')
            fg.load_extension('podcast')    
            print('2')
                
            fg.title('search results for '+' '.join(queries))
            print('3')
            
            if idx==0:
                fg.link(href='https://www.youtube.com/results?search_query='+queries[0].replace(' ',"+"), rel='self')
            else:
                fg.link(href='https://www.youtube.com/results?search_query='+queries[idx].replace(' ',"+"), rel='alternate')
            print("=====",fg.link)
            fg.description(description)
            fg.podcast.itunes_author = 'auto generated'
            fg.podcast.itunes_block = 'yes'
            fg.podcast.itunes_image = None
            fg.podcast.itunes_explicit = 'no'
            fg.podcast.itunes_complete = None
            fg.podcast.itunes_new_feed_url = None
            fg.podcast.itunes_owner = None
            fg.podcast.itunes_subtitle = "search results"
            fg.podcast.itunes_summary = None
            fg.podcast.itunes_category=None
            # fg.podcast.channel_title(info['channel'])
            for info in results:
            
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
        fg.rss_file(feedname+'.xml')
    return feedname+'.xml'

def url2rssURL(URL):
    if  "youtube.com" in URL:
        
        if URL.startswith('https://youtube.com/channel/') or URL.startswith("https://www.youtube.com/channel/"):

            channel_id=URL.split("channel/")[1]

            print("after replace---\n",channel_id)    

            # channel_id = 'UCBSQxFi6a8Ju2v_hgiM78Ew'
            if channel_id.endswith("/"):
                channel_id=channel_id.replace('/','')
            return "https://www.youtube.com/feeds/videos.xml?channel_id="+channel_id
        elif URL.startswith('https://www.youtube.com/results?search_query='):
# https://www.youtube.com/results?search_query=hammersmith+infant+neurological+examination+(hine)       
            queries=URL.split('https://www.youtube.com/results?search_query=')[-1]
            feedname=queries
            queries=[q.replace('+'," ") for q in queries.split('+or+')]
            print('grab keywords from search url',queries)
            rssurl=keywords2RssURL(queries,feedname)  
            return rssurl        
            
        else:

            # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
            ydl_opts = {
                'verbose': True,

            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                try:
                    info = ydl.extract_info(URL,download=False)
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

        # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
        ydl_opts = {
            'verbose': True,

        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            try:
                info = ydl.extract_info(URL,download=False)
                channel_id=info['channel_id']


                print("start processing---\n",URL)    
                if not os.path.exists(channel_id):
                    print('prepare dir:',channel_id)
                    os.mkdir(channel_id)
                rssurl = genrssfromchannel(URL)

            except Exception as e:  # skipcq: PYL-W0703
                print(e)

                return None      

def channel_id2rssurl(channel_id):
    return "https://www.youtube.com/feeds/videos.xml?channel_id="+channel_id
def genrssfromchannel(url):
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {
#         'outtmpl': videodir+'/%(title).200B%(title.201B&…|)s.%(ext)s',
#         'format': 'bestvideo[height<={}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[height<={}][ext=mp4][vcodec^=avc1]/best[ext=mp4]/best'.format(Height,Height),
        # 'proxy': 'socks5://127.0.0.1:1080'
        'verbose': True,

    }
    fg = FeedGenerator()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        try:
            info = ydl.extract_info(URL,download=False)
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
if Keywords:
    Keywords=remove_special_elements(Keywords)
    print(f"queries:{Keywords}")
    rssurl=keywords2RssURL(Keywords,'default')
else:
    rssurl = url2rssURL(URL)
print('we found rss url is :',rssurl)
