import os
from pytubefix import Channel,YouTube

folder_path = "./result"
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

URL = os.getenv("URL")
URL=URL.split('.com/')[-1]

def gettransp():

  c = Channel(f"https://www.youtube.com/{URL}")
  print(f'Downloading videos by: {c.channel_name}')

  for video in c.videos:
      print('===',video)
      id=video.video_id

      videourl = f'http://youtube.com/watch?v={id}'
      yt = YouTube(videourl)

      print('srt',yt.captions)
      if not yt.captions:
          caption = yt.captions['a.en']
          caption.save_captions(f"{id}.txt")
      else:
          print(f'there is no srt for {videourl}')
gettransp()
