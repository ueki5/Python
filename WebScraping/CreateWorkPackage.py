import requests
import json
from bs4 import BeautifulSoup
userid='apikey'
passwd='34739f806ab1b3caa301a77871a35600c1470ac8b13187bdb8b0c5fa1cad0404'
auth=(userid, passwd)
urlbase='http://192.168.99.100:30080/api/v3/'
subdir='work_packages/'
objid=''
url=urlbase+subdir+objid
headers={'Content-Type': 'application/json'}
data=json.dumps(
    {
        "subject":"暫定の仕事",
        "description": {
            "format": "textile",
            "raw": "日本語項目が登録できるか確認"
        },
        "project":{
            "href":"/api/v3/projects/2",
            "title":"Demo project"
        },
        "startDate":"2019-08-26",
        "dueDate":"2019-08-27",
        "estimatedTime":"PT4H",
        "percentageDone":39,
        "_links": {
            "type": {"href":"/api/v3/types/1"},
            "status":{"href":"/api/v3/statuses/1"},
            "priority":{"href":"/api/v3/priorities/1"}
        }
    })
html_doc = requests.post(url, data, headers=headers, auth=auth).text
soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
print(soup.prettify())