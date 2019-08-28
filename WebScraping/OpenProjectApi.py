import requests
import json
class OpenProjectApi:
    def __init__(self, hostname, passwd):
        self.__init__
        self.userid='apikey'
        self.passwd=passwd
        self.auth=(self.userid, self.passwd)
        self.protcol='http://'
        self.hostname = hostname
        self.apiroot='/api/v3/'
        self.headers={'Content-Type': 'application/json'}
    def get_url(self, objtype, objid):
        return (self.protcol + self.hostname + self.apiroot + objtype + '/' + objid)
    def get(self, objtype, objid):
        url=self.get_url(objtype, objid)
        doc = requests.get(url, headers=self.headers, auth=self.auth).text
        return json.loads(doc)
    def create(self, objtype, data):
        url=self.get_url(objtype, '')
        doc = requests.post(url, data, headers=self.headers, auth=self.auth).text
        return json.loads(doc)
    def update(self, objtype, objid, data):
        url=self.get_url(objtype, objid)
        doc = requests.patch(url, data, headers=self.headers, auth=self.auth).text
        return json.loads(doc)
    def delete(self, objtype, objid):
        url=self.get_url(objtype, objid)
        doc = requests.delete(url, headers=self.headers, auth=self.auth).text
        return json.loads(doc)
