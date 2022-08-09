


import os
from pytube import YouTube
import requests
import re
import json



#imp functions


def foldertitle(url):

    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text
    title = (re.finditer("<title>(.*)</title>",plain_text))
    return next(title).group(1).strip().lower().replace("|","").replace(" ","_").replace("\\","").replace("/","")
   

def link_snatcher(url):
    query = requests.get(url).text
    file = open("hello.html",'w',encoding='utf-8')
    file.write(query)
    file.close()
    jsonObject =json.loads(next(re.finditer("var ytInitialData = (\{.*\}\}\});\<",query)).group(1))
    contents = jsonObject["contents"]["twoColumnWatchNextResults"]["playlist"]["playlist"]
    title = contents["title"]
    print("title: " , title)
    contents = contents["contents"]
    DIR = os.getcwd()  + "\\" + foldertitle(url)
    for playlistItem in map(lambda x : x["playlistPanelVideoRenderer"] , contents[:-1]): 
        title = playlistItem["title"]["simpleText"]
        linkId = playlistItem["videoId"]
        print(f"\rtitle : {title} , id : {linkId} ",end="")
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
