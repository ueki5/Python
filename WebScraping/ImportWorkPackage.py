import json
import csv
import pprint
import pandas as pd
import OpenProjectApi

# 設定・定義
setpath = '.\\config\\setting.json'
usrpath = '.\\config\\users.json'
csvpath = '.\\config\\import_tasks.csv'

# CSVカラム定義
fieldnames = [
    'name', 
    'description', 
    'startDate', 
    'dueDate', 
    'estimatedTime', 
    'type', 
    'status', 
    'priority',
    'assignee',
    ]

# 設定ファイル読み込み
setfile = open(setpath, encoding='shift_jis')
setdic = json.load(setfile)
usrfile = open(usrpath, encoding='shift_jis')
usrdic = json.load(usrfile)
opnprj=OpenProjectApi.OpenProjectApi(setdic['hostname'], setdic['apikey'])
doc = opnprj.get('projects', setdic['projectid'])
print('{0}にタスクをインポートします。よろしいですか？(Y/N)'.format(doc['name']))
reply = input('>> ').upper()

# YESでなければ終了
if reply != 'Y':
    print('処理を終了します')
    exit

# CSVファイル読み込み
csvfile = open(csvpath, encoding='shift_jis')
reader = csv.DictReader(csvfile, 
        delimiter=',', 
        quotechar='"', 
        fieldnames=fieldnames,
        )

# 担当者チェック
users = pd.unique([task['assignee'] for task in reader])
for usr in users:
   reply = opnprj.get('users', usrdic[usr])
   print(reply)

# １件ずつタスクに変換し、REST APIて登録
for taskin in reader:
    # 登録用データ編集（辞書型）
    taskout = {}
    taskout['project'] = {'href': '/api/v3/projects/' 
                        + setdic['projectid']}
    taskout['subject'] = taskin['name']
    taskout['description'] = {
                            'format': 'textile',
                            'raw': taskin['description']}
    taskout['startDate'] = taskin['startDate']
    taskout['dueDate'] = taskin['dueDate']
    taskout['estimatedTime'] = taskin['estimatedTime']
    taskout['_links'] = {}
    taskout['_links']['type'] = {'href': '/api/v3/types/1'}
    taskout['_links']['status'] = {'href': '/api/v3/statuses/' 
                                    + taskin['status']}
    taskout['_links']['priority'] = {'href': '/api/v3/priorities/' 
                                    + taskin['priority']}
    taskout['_links']['assignee'] = {'href':'/api/v3/users/' 
                                    + usrdic[taskin['assignee']]}
#    # REST API CREATEメソッド呼び出し
#    reply = opnprj.create('work_packages', json.dumps(taskout))
#    print(reply)
