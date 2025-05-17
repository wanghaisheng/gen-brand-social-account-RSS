import os
from pytubefix import Channel,YouTube

folder_path = "./result"
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

URL = os.getenv("URL")

def gettransp():

  c = Channel("https://www.youtube.com/@ProgrammingKnowledge")
  print(f'Downloading videos by: {c.channel_name}')

  for video in c.videos:
      print('===',video)
      id=video.videoId

      yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
      print(yt.captions)
      t=yt.captions
      with open(folder_path+'/'+id + ".txt", "w", encoding="utf8") as f:
        f.write(t)
gettransp()
