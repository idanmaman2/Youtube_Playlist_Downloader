


import os
from pytube import YouTube
import json
import ytjson
import threading
import time 
from collections import deque
import enum
THREADS = 10 
songsQeue = deque(tuple())
waiting = True 
class Res(enum.Enum):
    AudioHigh = 1
    AudioLow = 2
    AudioFirst = 3
    VideoHighRes = 4 
    VidoeLowRes = 5 
    ViedoHighFps = 6
    VideoLowFps = 7
    VideoFirst = 8 

def Downloadtask(): 
    while songsQeue or  waiting   : 
        if songsQeue : 
            stream, title = songsQeue.pop()
            try : 
                print(f"downlading {title}")
                stream.download(title)
                print(f"downloaded {title}")
            except : 
                print ( title , "failed", sep ="-", end= f"\n{ ('*' * 10) } \n")
        elif waiting :                
            time.sleep(0.5)

def link_snatcher(url:str ,res : Res ):
    jsonObject = ytjson.get_ytJson(url)
    contents = jsonObject["contents"]["twoColumnWatchNextResults"]["playlist"]["playlist"]
    title = contents["title"]
    print("title: " , title)
    contents = contents["contents"]
    dir = os.getcwd() + f"/Quality{res}" + "/"+  title
    for playlistItem in map(lambda x : x["playlistPanelVideoRenderer"] , contents[:-1]): 
        titleLocal = playlistItem["title"]["simpleText"]
        linkId = playlistItem["videoId"]
        print(f"\rtitle : {titleLocal} , id : {linkId} ",end="")
        yt = YouTube(f"http://youtube.com/watch?v={linkId}")
        stream = None
        match(res):
            case Res.AudioHigh : 
                 stream =max(yt.streams.filter(type="audio"),key=lambda x : x.abr)
            case Res.AudioLow:
                stream =min(yt.streams.filter(type="audio"),key=lambda x : x.abr)
            case Res.AudioFirst:
                stream = yt.streams.filter(type="audio").first()
            case Res.VideoHighRes:
                stream =max(yt.streams.filter(type="video"),key=lambda x : x.resolution)
            case Res.VidoeLowRes:
                stream =min(yt.streams.filter(type="video"),key=lambda x : x.resolution)
            case Res.ViedoHighFps:
                stream =max(yt.streams.filter(type="video"),key=lambda x : x.fps)
            case Res.VideoLowFps:
                stream =min(yt.streams.filter(type="video"),key=lambda x : x.fps)
            case Res.AudioFirst:
                stream = yt.streams.filter(type="video").first()
        songsQeue.appendleft((stream,dir))
        
        
file_name = input("enter json with links path: ")
jsObject = json.load(open(file_name,'r'))
print(*list(Res),sep="\n")
quality = Res(int(input("quality: ")))
threads =[threading.Thread(target = Downloadtask) for i in range(THREADS)]
for tr in threads : 
    tr.start()
for link in jsObject["links"]: 
    try : 
        link_snatcher(link,quality)
    except Exception as err:
        print(err)
        print(link + " failed")
waiting = False 
for i in threads: 
    tr.join() 

