import requests
import json
from bs4 import BeautifulSoup
class OpenProjectApi:
    def __init__(self, hostname=None):
        self.__init__
        self.userid='apikey'
        self.passwd='4c822580dcf5a49c9a63ffa3380f8bfd7b6c48e1656f7392ac9de1b821319bc0'
        self.auth=(self.userid, self.passwd)
        self.protcol='http://'
        if hostname is None:
            hostname='192.168.99.100:30080'
        self.hostname = hostname
        self.apiroot='/api/v3/'
        self.headers={'Content-Type': 'application/json'}
    def get_url(self, objtype, objid):
        return (self.protcol + self.hostname + self.apiroot + objtype + '/' + objid)
    def get(self, objtype, objid):
        url=self.get_url(objtype, objid)
        html_doc = requests.get(url, headers=self.headers, auth=self.auth).text
        return BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
    def create(self, objtype, data):
        url=self.get_url(objtype, '')
        html_doc = requests.post(url, data, headers=self.headers, auth=self.auth).text
        return BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
    def update(self, objtype, objid, data):
        url=self.get_url(objtype, objid)
        html_doc = requests.patch(url, data, headers=self.headers, auth=self.auth).text
        return BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
    def delete(self, objtype, objid):
        url=self.get_url(objtype, objid)
        html_doc = requests.delete(url, headers=self.headers, auth=self.auth).text
        return BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
