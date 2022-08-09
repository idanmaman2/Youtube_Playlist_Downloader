import json
import requests
import re
import ytjson
def getjson(url): 
  jsonObject=ytjson.get_ytJson(url)
  dictRes = {"links" : None }
  tabRenderers = jsonObject["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
  tabRenderRes= next(filter(lambda packet :"content" in  packet["tabRenderer"],tabRenderers ))
  playlists = tabRenderRes["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["gridRenderer"]["items"]
  listRes = map(lambda pack : pack["gridPlaylistRenderer"]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]  ,filter(lambda x : "gridPlaylistRenderer" in x , playlists) )
  dictRes["links"] = list(map(lambda linkId: f"http://youtube.com{linkId}" , listRes))
  return dictRes  


file = open("playlist_dumps.json",'w',encoding='utf-8')
file.write(json.dumps(getjson("https://www.youtube.com/channel/UC8DT6_qCiFpANeZ242oSmwg/playlists")))
file.close()