import requests
import json
from bs4 import BeautifulSoup
import OpenProjectApi
data=json.dumps(
    {
        "project":{
            "href":"/api/v3/projects/3"
        },
        "subject":"テストタスク",
        "description": {
            "format": "textile",
            "raw": "登録形式確認用"
        },
        "startDate":"2019-08-28",
        "dueDate":"2019-08-29",
        "estimatedTime":"PT8H",
        "_links": {
            "type": {"href":"/api/v3/types/1"},
            "status":{"href":"/api/v3/statuses/8"},
            "priority":{"href":"/api/v3/priorities/1"},
            "assignee":{"href":"/api/v3/users/5"}
        }
    })
opnprj=OpenProjectApi.OpenProjectApi()
soup=opnprj.create('work_packages', data)
print(soup.prettify())