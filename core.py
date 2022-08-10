


import os
from pytube import YouTube
import json
import ytjson

import enum
 
class Res(enum.Enum):
    AudioHigh = 1
    AudioLow = 2
    AudioFirst = 3
    VideoHighRes = 4 
    VidoeLowRes = 5 
    ViedoHighFps = 6
    VideoLowFps = 7
    VideoFirst = 8 

def link_snatcher(url:str ,res : Res):
    jsonObject = ytjson.get_ytJson(url)
    contents = jsonObject["contents"]["twoColumnWatchNextResults"]["playlist"]["playlist"]
    title = contents["title"]
    print("title: " , title)
    contents = contents["contents"]
    DIR = os.getcwd()+f"\\Quality{res}" + "\\"+  ytjson.get_title(url)
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
                stream =max(yt.streams.filter(type="video"),key=lambda x : x.res)
            case Res.VidoeLowRes:
                stream =min(yt.streams.filter(type="video"),key=lambda x : x.res)
            case Res.ViedoHighFps:
                stream =max(yt.streams.filter(type="video"),key=lambda x : x.fps)
            case Res.VideoLowFps:
                stream =min(yt.streams.filter(type="video"),key=lambda x : x.fps)
            case Res.AudioFirst:
                stream = yt.streams.filter(type="video").first()
            
        stream.download(DIR)
file_name = input("enter json with links path: ")
jsObject = json.load(open(file_name,'r'))
quality = Res(int(input("quality: ")))
for link in jsObject["links"]: 
    try : 
        link_snatcher(link,quality)
    except Exception as err:
        print(err)
        print(link + " failed")
