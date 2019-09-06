import requests
import json
import OpenProjectApi
opnprj=OpenProjectApi.OpenProjectApi('192.168.99.100:30080', 'bb5be3efe44f3e954ccaebe244c5ba72e0f2ee8bdb5220723db3b92606b1cccb')
soup=opnprj.get('users', '')
print(json.dumps(soup))