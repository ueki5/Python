import requests
import json
from bs4 import BeautifulSoup
import OpenProjectApi
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
opnprj=OpenProjectApi.OpenProjectApi()
soup=opnprj.create('work_packages', data)
print(soup.prettify())