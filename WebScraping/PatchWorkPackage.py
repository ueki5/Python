import requests
import json
from bs4 import BeautifulSoup
userid='apikey'
passwd='34739f806ab1b3caa301a77871a35600c1470ac8b13187bdb8b0c5fa1cad0404'
url='http://192.168.99.100:30080/api/v3/work_packages/'
workpkg_id='42'
data=json.dumps({"description":{"format":"markdown","raw":"null","html":""},"_embedded":{"attachments":{"_type":"Collection","total":0,"count":0,"_embedded":{"elements":[]},"_links":{"self":{"href":"/api/v3/work_packages/42/attachments"}}},"watchers":{"_type":"Collection","total":0,"count":0,"_embedded":{"elements":[]},"_links":{"self":{"href":"/api/v3/work_packages/42/watchers"}}},"relations":{"_type":"Collection","total":7,"count":7,"_embedded":{"elements":[{"_type":"Relation","id":76,"name":"translation missing: ja.label_","delay":"null","description":"null","_links":{"self":{"href":"/api/v3/relations/76"},"updateImmediately":{"href":"/api/v3/relations/76","method":"patch"},"delete":{"href":"/api/v3/relations/76","method":"delete","title":"Remove relation"},"from":{"href":"/api/v3/work_packages/42","title":"RedMineセットアップ"},"to":{"href":"/api/v3/work_packages/42","title":"RedMineセットアップ"}}},{"_type":"Relation","id":77,"name":"次の項目に後続","type":"follows","reverseType":"precedes","delay":"null","description":"null","_links":{"self":{"href":"/api/v3/relations/77"},"updateImmediately":{"href":"/api/v3/relations/77","method":"patch"},"delete":{"href":"/api/v3/relations/77","method":"delete","title":"Remove relation"},"from":{"href":"/api/v3/work_packages/42","title":"RedMineセットアップ"},"to":{"href":"/api/v3/work_packages/22","title":"Develop v2.0"}}},{"_type":"Relation","id":78,"name":"次の項目に後続","type":"follows","reverseType":"precedes","delay":"null","description":"null","_links":{"self":{"href":"/api/v3/relations/78"},"updateImmediately":{"href":"/api/v3/relations/78","method":"patch"},"delete":{"href":"/api/v3/relations/78","method":"delete","title":"Remove relation"},"from":{"href":"/api/v3/work_packages/42","title":"RedMineセットアップ"},"to":{"href":"/api/v3/work_packages/7","title":"Create wireframes for new landing page"}}},{"_type":"Relation","id":93,"name":"次の項目に後続","type":"follows","reverseType":"precedes","delay":"null","description":"null","_links":{"self":{"href":"/api/v3/relations/93"},"updateImmediately":{"href":"/api/v3/relations/93","method":"patch"},"delete":{"href":"/api/v3/relations/93","method":"delete","title":"Remove relation"},"from":{"href":"/api/v3/work_packages/42","title":"RedMineセットアップ"},"to":{"href":"/api/v3/work_packages/18","title":"Develop v1.0"}}},{"_type":"Relation","id":94,"name":"次の項目に後続","type":"follows","reverseType":"precedes","delay":"null","description":"null","_links":{"self":{"href":"/api/v3/relations/94"},"updateImmediately":{"href":"/api/v3/relations/94","method":"patch"},"delete":{"href":"/api/v3/relations/94","method":"delete","title":"Remove relation"},"from":{"href":"/api/v3/work_packages/42","title":"RedMineセットアップ"},"to":{"href":"/api/v3/work_packages/19","title":"Release v1.0"}}},{"_type":"Relation","id":95,"name":"次の項目に後続","type":"follows","reverseType":"precedes","delay":"null","description":"null","_links":{"self":{"href":"/api/v3/relations/95"},"updateImmediately":{"href":"/api/v3/relations/95","method":"patch"},"delete":{"href":"/api/v3/relations/95","method":"delete","title":"Remove relation"},"from":{"href":"/api/v3/work_packages/42","title":"RedMineセットアップ"},"to":{"href":"/api/v3/work_packages/20","title":"Develop v1.1"}}},{"_type":"Relation","id":96,"name":"次の項目に後続","type":"follows","reverseType":"precedes","delay":"null","description":"null","_links":{"self":{"href":"/api/v3/relations/96"},"updateImmediately":{"href":"/api/v3/relations/96","method":"patch"},"delete":{"href":"/api/v3/relations/96","method":"delete","title":"Remove relation"},"from":{"href":"/api/v3/work_packages/42","title":"RedMineセットアップ"},"to":{"href":"/api/v3/work_packages/21","title":"Release v1.1"}}}]},"_links":{"self":{"href":"/api/v3/work_packages/42/relations"}}},"type":{"_type":"Type","id":1,"name":"Task","color":"#1A67A3","position":1,"isDefault":"true","isMilestone":"false","createdAt":"2019-08-24T11:51:19Z","updatedAt":"2019-08-24T11:51:19Z","_links":{"self":{"href":"/api/v3/types/1","title":"Task"}}},"priority":{"_type":"Priority","id":8,"name":"Normal","position":2,"color":"#D3F9D8","isDefault":"true","isActive":"true","_links":{"self":{"href":"/api/v3/priorities/8","title":"Normal"}}},"project":{"_type":"Project","id":1,"identifier":"your-scrum-project","name":"Scrum project","description":"*This is a Scrum demo project.*\nYou can edit the project description in the [Project settings -&gt; Description](/projects/your-scrum-project/settings).\n","createdAt":"2019-08-24T11:51:29Z","updatedAt":"2019-08-24T11:51:29Z","_links":{"self":{"href":"/api/v3/projects/1","title":"Scrum project"},"createWorkPackage":{"href":"/api/v3/projects/1/work_packages/form","method":"post"},"createWorkPackageImmediate":{"href":"/api/v3/projects/1/work_packages","method":"post"},"categories":{"href":"/api/v3/projects/1/categories"},"versions":{"href":"/api/v3/projects/1/versions"},"types":{"href":"/api/v3/projects/1/types"}}},"status":{"_type":"Status","id":1,"name":"New","isClosed":"false","color":"#C3FAE8","isDefault":"true","isReadonly":"false","defaultDoneRatio":"null","position":1,"_links":{"self":{"href":"/api/v3/statuses/1","title":"New"}}},"author":{"_type":"User","id":3,"name":"植木 豪","createdAt":"2019-08-24T11:57:48Z","updatedAt":"2019-08-24T16:09:39Z","login":"ueki5@fujitsu.com","admin":"true","firstName":"豪","lastName":"植木","email":"null","avatar":"http://gravatar.com/avatar/e1e7b0caec2b78c86a4cdb6d7a33f87f?default=404&amp;secure=false","status":"active","identityUrl":"null","_links":{"self":{"href":"/api/v3/users/3","title":"植木 豪"},"showUser":{"href":"/users/3","type":"text/html"},"updateImmediately":{"href":"/api/v3/users/3","title":"Update ueki5@fujitsu.com","method":"patch"},"lock":{"href":"/api/v3/users/3/lock","title":"Set lock on ueki5@fujitsu.com","method":"post"}}},"customActions":[]},"_type":"WorkPackage","id":42,"lockVersion":9,"subject":"RedMineセットアップ","startDate":"2019-09-19","dueDate":"2019-09-25","estimatedTime":"null","percentageDone":0,"createdAt":"2019-08-24T15:05:43Z","updatedAt":"2019-08-24T15:11:28Z","remainingTime":"null","_links":{"attachments":{"href":"/api/v3/work_packages/42/attachments"},"addAttachment":{"href":"/api/v3/work_packages/42/attachments","method":"post"},"self":{"href":"/api/v3/work_packages/42","title":"RedMineセットアップ"},"update":{"href":"/api/v3/work_packages/42/form","method":"post"},"schema":{"href":"/api/v3/work_packages/schemas/1-1"},"updateImmediately":{"href":"/api/v3/work_packages/42","method":"patch"},"delete":{"href":"/api/v3/work_packages/42","method":"delete"},"move":{"href":"/work_packages/42/move/new","type":"text/html","title":"Move RedMineセットアップ"},"copy":{"href":"/work_packages/42/copy","title":"Copy RedMineセットアップ"},"pdf":{"href":"/work_packages/42.pdf","type":"application/pdf","title":"Export as PDF"},"atom":{"href":"/work_packages/42.atom","type":"application/rss+xml","title":"Atom feed"},"availableRelationCandidates":{"href":"/api/v3/work_packages/42/available_relation_candidates","title":"Potential work packages to relate to"},"customFields":{"href":"/projects/your-scrum-project/settings/custom_fields","type":"text/html","title":"Custom fields"},"configureForm":{"href":"/types/1/edit?tab=form_configuration","type":"text/html","title":"Configure form"},"activities":{"href":"/api/v3/work_packages/42/activities"},"availableWatchers":{"href":"/api/v3/work_packages/42/available_watchers"},"relations":{"href":"/api/v3/work_packages/42/relations"},"revisions":{"href":"/api/v3/work_packages/42/revisions"},"watchers":{"href":"/api/v3/work_packages/42/watchers"},"addWatcher":{"href":"/api/v3/work_packages/42/watchers","method":"post","payload":{"user":{"href":"/api/v3/users/{user_id}"}},"templated":true},"removeWatcher":{"href":"/api/v3/work_packages/42/watchers/{user_id}","method":"delete","templated":true},"addRelation":{"href":"/api/v3/work_packages/42/relations","method":"post","title":"Add relation"},"addChild":{"href":"/api/v3/projects/your-scrum-project/work_packages","method":"post","title":"Add child of RedMineセットアップ"},"changeParent":{"href":"/api/v3/work_packages/42","method":"patch","title":"Change parent of RedMineセットアップ"},"addComment":{"href":"/api/v3/work_packages/42/activities","method":"post","title":"Add comment"},"previewMarkup":{"href":"/api/v3/render/markdown?context=/api/v3/work_packages/42","method":"post"},"category":{"href":"null"},"type":{"href":"/api/v3/types/1","title":"Task"},"priority":{"href":"/api/v3/priorities/8","title":"Normal"},"project":{"href":"/api/v3/projects/1","title":"Scrum project"},"status":{"href":"/api/v3/statuses/1","title":"New"},"author":{"href":"/api/v3/users/3","title":"植木 豪"},"responsible":{"href":"null"},"assignee":{"href":"null"},"version":{"href":"null"},"watch":{"href":"/api/v3/work_packages/42/watchers","method":"post","payload":{"user":{"href":"/api/v3/users/3"}}},"ancestors":[],"parent":{"href":"null","title":"null"},"customActions":[]}})
html_doc = requests.patch(url + workpkg_id, data, headers={'Content-Type': 'application/hal+json'}, auth=(userid, passwd)).text
soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
print(soup.prettify())