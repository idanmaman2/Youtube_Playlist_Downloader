import json 
import requests 
import re 
def get_ytJson(url):
    try:
        query = requests.get(url).text
    except:
        raise Exception(':( - skynet overrite all of your computer - just joking there is no internet ')
        
    return json.loads(next(re.finditer("var ytInitialData = (\{.*\}\}\});\<",query)).group(1))
def get_title(url):
    try:
        res = requests.get(url)
    except:
        raise Exception(':( - skynet overrite all of your computer - just joking there is no internet ')
    plain_text = res.text
    title = (re.finditer("<title>(.*) - YouTube</title>",plain_text))
    return next(title).group(1).strip().lower().replace("|","").replace(" ","_").replace("\\","").replace("/","")
