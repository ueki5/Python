import json
import pandas
# f = open('C:\\opt\\社内\\社内活動\\20190827_OpenProject\\users.json', 'r')
# jsonData = json.load(f)
# f.close()
names = ["タスク名", "概要", "開始日", "終了日", "見積時間", "種別", "状態", "優先度", "担当者"]
df = pandas.read_csv(
    'C:\\opt\\社内\\社内活動\\20190827_OpenProject\\keigen_zeiritsu.csv', 
    encoding='shift_jis', 
    header=None, names=names)
# print(df)
tasknames = df["タスク名"]
# print(tasknames)
# for wp in tasknames:
for wp in df:
     print(wp[0])
