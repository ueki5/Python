import json
import pprint
# import csv
# import pandas
filename = 'C:\\opt\\社内\\社内活動\\20190827_OpenProject\\users.json'
jsonfile = open(filename, 'r')
obj = json.load(jsonfile)
for key, value in obj.items():
    print(key)
# f = open('C:\\opt\\社内\\社内活動\\20190827_OpenProject\\users.json', 'r')
# jsonData = json.load(f)
# f.close()
# names = ["タスク名", "概要", "開始日", "終了日", "見積時間", "種別", "状態", "優先度", "担当者"]
# df = pandas.read_csv(
#     'C:\\opt\\社内\\社内活動\\20190827_OpenProject\\keigen_zeiritsu.csv', 
#     encoding='shift_jis', 
#     header=None, names=names)
# print(df)
# tasknames = df["タスク名"]
# print(tasknames)
# for wp in tasknames:
# for wp in df:
#      print(wp[0])
# fieldnames = ["タスク名", "概要", "開始日", "終了日", "見積時間", "種別", "状態", "優先度", "担当者"]
# filename = 'C:\\opt\\社内\\社内活動\\20190827_OpenProject\\keigen_zeiritsu.csv'
# with open(filename, newline='', encoding='shift_jis') as csvfile:
#     reader = csv.DictReader(csvfile, 
#         delimiter=',', 
#         quotechar='"', 
#         fieldnames=fieldnames,
#         )
#     for row in reader:
#         print(row["タスク名"])
