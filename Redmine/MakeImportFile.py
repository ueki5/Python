import os
import sys
import argparse
import datetime
import re
import json
import csv
import pandas as pd
import numpy as np
from redminelib import Redmine

###################################################
# 設定・定義
###################################################
cfgpath = ""
csvtktpath = ""
# CSV書き込み項目
csvfmt = {
    "TicketNumber": 0,
    "subject": 1,
    "priority": 3,
    "status": 4,
    "Type": 5,
    "CustomerID": 7,
    "CustomerUser": 8,
    "assigned_to": 9,
    "start_date": 10,
    "due_date": 11,
    "DynamicField_IncidentType": 12,
    "DynamicField_TaiouKousuu": 13,
    "DynamicField_XITSMCloseDate": 14,
    "DynamicField_XITSMGeneralTextarea1": 15,
    "DynamicField_XITSMGeneralTextarea3": 16,
    "DynamicField_ProjectSpecific": 17
}
#################################################
# 関数
###################################################
# 26進変換
n_ary=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

# Excel列指定変換ヘルパー関数
def _idxToA1(unit, ary, inp):
    nextAry = ary+[n_ary[inp%unit]]
    nextInp = int(inp/unit)
    return (nextAry, nextInp)
# Excel列指定変換
def idxToA1(idx):
    unit = len(n_ary)
    out = []
    inp = idx
    while True:
        (nextOut, nextInp) = _idxToA1(unit, out, inp)
        # 配列が追加がされていて、入力に変更がなければ終了
        if len(out)>0 and inp == nextInp:
            break
        else:
            out = nextOut
            inp = nextInp
    return "".join(list(reversed(out)))
# Excel列指定逆変換
def a1ToIdx(a1):
    unit = len(n_ary)
    # 表記を逆順にして配列化("AC" -> ["C", "A"])
    chrAry = list(reversed(a1))
    # 表記配列の桁位置を配列化 ["C", "A"] -> [0, 1]
    posAry = list(range(len(chrAry)))
    # 表記から値を求める辞書を作成 {"A":1, "B":2, … "Z":26}
    valDic = {n_ary[i]:i+1 for i in range(len(n_ary))}
    # 10進数に変換（Cの意味する値(3) * 26^0 + Aの意味する値(1) * 26^1）
    return rowToIdx(sum([valDic[chr]*pow(unit,pos) for chr, pos in zip(chrAry, posAry)]))
# Excel行指定変換
def idxToRow(idx):
    return idx+1
# Excel行指定逆変換
def rowToIdx(row):
    return row-1
# 行列指定方法変換
def cnvColRowFormula(fnRow, fnCol):
    # 開始行
    prjinf["ticketinfo"]["startrow"] = fnRow(prjinf["ticketinfo"]["startrow"])
    # コラム（列）位置
    for key, val in prjinf["ticketinfo"]["format"].items():
        if key == "DynamicField_ProjectSpecific":
            # 複数項目を保持している為、子要素に対して変換を行う
            for key2, val2 in prjinf["ticketinfo"]["format"]["DynamicField_ProjectSpecific"].items():
                prjinf["ticketinfo"]["format"]["DynamicField_ProjectSpecific"][key2] = fnCol(val2)
        else:
            prjinf["ticketinfo"]["format"][key] = fnCol(val)
# 値の有効判定
def isvalidval(val):
    return val is not None and val==val # None,nanは無効値
# 行の有効判定
def isvalidrec(idx, lst):
    return idx >= prjinf["ticketinfo"]["startrow"] and isvalidval(lst[prjinf["ticketinfo"]["format"][prjinf["ticketinfo"]["checkclm"]]])
# 全項目を保持するリストから、必要項目だけを含む辞書型（KEY=項目名）に変換
def shrinkclm(lst):
    dic = {}
    for key, val in prjinf["ticketinfo"]["format"].items():
        if isinstance(val, int):
            # 単項目の場合
            dic[key] = lst[val]
        else:
            # 複合項目の場合、JSON風の形式で詰め込む
            clmval = ""
            for subkey, subval in val.items():
                clmval += ", " if len(clmval) > 0 else ""
                clmval += subkey + ":"
                clmval += conv2str(lst[subval])
            # 改行はスペースに変換
            clmval = re.sub("\n|\r\n"," ", clmval)
            dic[key] = clmval
    return dic
# 文字列化
def conv2str(val):
    return ("{0:%Y/%m/%d %H:%M:%S}".format(val) if isinstance(val, datetime.date) 
            else "{0:%H:%M:%S}".format(val) if isinstance(val, datetime.time) 
            else str(val) if isvalidval(val) 
            else "")
# 日付変換
def conv2date(str):
    return (datetime.datetime.strptime(str, "%Y/%m/%d %H:%M:%S").date() if len(str) == 19 
            else "")
# 書き出し用レコード作成
def conv2csvfmt(srcdic):
    dstdic = {}
    # 読み込み項目転記
    for key,val in srcdic.items():
        dstdic[key] = conv2str(val)
    # 不足項目初期化
    for key in csvfmt.keys():
        dstdic.setdefault(key, "")
    return dstdic
# 項目値の重複を除き、項目値をキーとする辞書を作成
def uniquedic(keywds, recs):
    lst = []
    for keywd in keywds:
        lst = lst + [rec[keywd] for rec in recs]
    return {uniqrec:"" for uniqrec in np.unique(lst)}
# 項目マッピング用変換マスタに不足分を追加
def addmst(dstdic, mstkey, srcdic):
    dstdic.setdefault(mstkey, {})
    for key, val in srcdic.items():
        dstdic[mstkey].setdefault(key, val)
# 項目変換
def cnvval(dic, val):
   return dic[val] if len(dic) > 0 else val 
# レコード変換
def cnvrec(rec):
    rec["TicketNumber"] = prjinf["TicketNumber"]["Prefix"] + rec["TicketNumber"].zfill(prjinf["TicketNumber"]["Length"])
    rec["priority"] = cnvval(prjinf["mstPriority"], rec["priority"])
    rec["status"] = cnvval(prjinf["mstStatus"], rec["status"])
    rec["CustomerID"] = prjinf["CustomerID"]
    rec["CustomerUser"] = cnvval(prjinf["mstCustomerUser"], rec["CustomerUser"])
    rec["assigned_to"] = cnvval(prjinf["mstUser"], rec["assigned_to"])
    rec["DynamicField_IncidentType"] = cnvval(prjinf["mstIncidentType"], rec["DynamicField_IncidentType"])
    for key,val in prjinf["ticketinfo"]["replaceclm"].items():
        rec[key] = re.sub(val["regexp"],val["repval"], rec[key])
    return rec
# イシュー登録
def updIssue(rec):
    issue = getIssue(rec["TicketNumber"])
    # 既存イシューの場合、作業時間、コメントの更新
    if issue.id != 0:
        # 作業時間の更新
        updTimeEntry(issue.id)
        # コメントの更新
        updNotes(issue.id)
    issue.project_id = project.id
    issue.subject = rec["subject"]
    issue.tracker_id = 3     #サービス固定
    issue.status_id = 1      #ステータス
    issue.priority_id = 1    #優先度
    issue.assigned_to_id = 1 #担当者のID
    issue.start_date = conv2date(rec["start_date"]) #開始日
    issue.due_date = conv2date(rec["due_date"])   #期日
    issue.estimated_hours = 4   # 予想工数
    issue.custom_fields = [{'id': 7, 'value': rec["TicketNumber"]}]
    issue.save()
# イシュー取得
def getIssue(external_key):
    issues = redmine.issue.filter(project_id = project.id, cf_7 = external_key)
    return issues[0] if len(issues) > 0 else redmine.issue.new()
# 作業時間更新（暫定コード）
def updTimeEntry(issue_id):
    time_entries = redmine.time_entry.filter(project_id = project.id, issue_id = issue_id)
    for time_entry in time_entries:
        time_entry.spent_on = datetime.date(2014, 1, 31)
        time_entry.hours = 99
        time_entry.activity_id = 10
        time_entry.comments = 'hello!'
        time_entry.save()
# コメント更新（delete,updateできないので追加のみ）（暫定コード）
def updNotes(issue_id):
    time_entries = redmine.time_entry.filter(project_id = project.id, issue_id = issue_id)
    for time_entry in time_entries:
        time_entry.spent_on = datetime.date(2014, 1, 31)
        time_entry.hours = 99
        time_entry.activity_id = 10
        time_entry.comments = 'hello!'
###################################################
# メイン処理
###################################################
# 引数チェック
parser = argparse.ArgumentParser()
parser.add_argument("projectid")
args = parser.parse_args()
cfgpath = args.projectid + ".json"
csvtktpath = args.projectid + "_tickets.csv"

# 設定ファイル存在チェック
if not(os.path.isfile(cfgpath)):
    # 存在しない場合、メッセージ表示して終了
    print("設定ファイル（{}）が存在しない為、終了します。\n".format(cfgpath))
    sys.exit(1)
# 設定ファイル読み込み
with open(cfgpath, encoding="utf-8", mode="r") as jsnfile:
    prjinf = json.load(jsnfile)
#####################################################
# 基本項目
#####################################################
apiUrl = prjinf["apiUrl"]
apiKey = prjinf["apiKey"]
#####################################################
# 行列指定方法変換（Excel方式からインデックス方式へ）
#####################################################
cnvColRowFormula(rowToIdx, a1ToIdx)
# EXCELファイル読み込み
exlfile = pd.read_excel(prjinf["bookname"], sheet_name=prjinf["ticketinfo"]["sheetname"], header=None)
# 有効行のみ、必要項目だけを抜き出す
exlrecs = [conv2csvfmt(shrinkclm(exlrec)) 
            for idx, exlrec in enumerate(exlfile.values) 
            if isvalidrec(idx, exlrec)]
# 優先度マッピング追加
addmst(prjinf, "mstPriority", uniquedic(["priority"],exlrecs))
# 状態マッピング追加
addmst(prjinf, "mstStatus", uniquedic(["status"],exlrecs))
# 利用者マッピング追加
addmst(prjinf, "mstCustomerUser", uniquedic(["CustomerUser"],exlrecs))
# 運用者マッピング追加
addmst(prjinf, "mstUser", uniquedic(["assigned_to"],exlrecs))
# インシデント分類マッピング追加
addmst(prjinf, "mstIncidentType", uniquedic(["DynamicField_IncidentType"],exlrecs))
#####################################################
# 行列指定方法戻し（インデックス方式からExcel方式へ）
#####################################################
cnvColRowFormula(idxToRow, idxToA1)
# JSONファイル書き込み
with open(cfgpath, encoding="utf-8", mode="w") as jsnfile:
    json.dump(prjinf, jsnfile, ensure_ascii=False, indent=4)
# サーバ接続
redmine = Redmine(apiUrl, key=apiKey)
project = redmine.project.get(prjinf["CustomerID"])
# CSVファイル書き込み
with open(csvtktpath, encoding="utf-8", newline='', mode='w') as csvtktfile:
    csvwriter = csv.DictWriter(
                            csvtktfile,
                            fieldnames=list(csvfmt.keys()), 
                            delimiter=',', 
                            quotechar='"',
                            lineterminator='\n', 
                            quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writeheader()
    for rec in exlrecs:
        recw = cnvrec(rec)
        csvwriter.writerow(recw)
        updIssue(recw)
print("インポート用のCSV（{}）が作成されました。\n".format(csvtktpath))
# 終了メッセージ
print("処理が完了しました\n")
