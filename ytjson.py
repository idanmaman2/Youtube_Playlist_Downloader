import json 
import requests 
import re 
def get_ytJson(url):
    try:
        query = requests.get(url).text
    except Exception as e:
        raise Exception(':( - skynet overrite all of your computer - just joking there is no internet ' + e )
    try : 
        return json.loads(next(re.finditer("var ytInitialData = (\{.*\}\}\});\<\/script>",query)).group(1))
    except : 
        return None
def get_title(url):
    try:
        res = requests.get(url)
    except Exception as e:
        raise Exception(':( - skynet overrite all of your computer - just joking there is no internet ' + e )
    plain_text = res.text
    title = (re.finditer("<title>(.*) - YouTube</title>",plain_text))
    return next(title).group(1).strip().lower().replace("|","").replace(" ","_").replace("\\","").replace("/","")
