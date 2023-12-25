import json
import ytjson

def getjson(url): 
  jsonObject=ytjson.get_ytJson(url)
  dictRes = {"links" : None }
  tabRenderers = jsonObject["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
  tabRenderRes= next(filter(lambda packet :"content" in  packet["tabRenderer"],tabRenderers ))
  playlists = tabRenderRes["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]
  if "gridRenderer" in playlists : 
    playlists = playlists["gridRenderer"]["items"]
  else : 
    playlists = playlists["shelfRenderer"]["content"]["horizontalListRenderer"]["items"]
  listRes = map(lambda pack : pack["gridPlaylistRenderer"]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]  ,filter(lambda x : "gridPlaylistRenderer" in x , playlists) )
  dictRes["links"] = list(map(lambda linkId: f"http://youtube.com{linkId}" , listRes))
  return dictRes  

    
file = open("playlist_dumps.json",'w',encoding='utf-8')
dumps = json.dumps(getjson(input("https://www.youtube.com/@VEVO/playlists")))
file.write(dumps)
print(dumps)
file.close()