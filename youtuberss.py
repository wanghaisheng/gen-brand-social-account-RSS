
import yt_dlp



URL = os.getenv('URL')




def youtubechannelrssfromurl(URL):


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
    else:
        print('invalid url')
        return None
