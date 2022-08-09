#!python3
# Usage -
# 1. open cmd
# 2. cd to the folder where these files are present
# 3. type - python ytdown.py
# the script will start working


import os
from pytube import YouTube
import requests
import re
import json
import ytjson
def link_snatcher(url):
    jsonObject = ytjson.get_ytJson(url)
    contents = jsonObject["contents"]["twoColumnWatchNextResults"]["playlist"]["playlist"]
    title = contents["title"]
    print("title: " , title)
    contents = contents["contents"]
    DIR = os.getcwd()  + "\\" + ytjson.get_title(url)
    for playlistItem in map(lambda x : x["playlistPanelVideoRenderer"] , contents[:-1]): 
        titleLocal = playlistItem["title"]["simpleText"]
        linkId = playlistItem["videoId"]
        print(f"\rtitle : {titleLocal} , id : {linkId} ",end="")
        yt = YouTube(f"http://youtube.com/watch?v={linkId}")
        stream = yt.streams.filter(type="audio",mime_type="audio/webm").first()
        stream.download(DIR)
file_name = input("enter json with links path")
jsObject = json.load(open(file_name,'r'))
for link in jsObject["links"]: 
    try : 
        link_snatcher(link)
    except Exception as err:
        print(err)
        print(link + " failed")