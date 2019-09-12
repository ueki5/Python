import os
import sys
import argparse
import datetime
import re
import json
import csv
import pandas as pd
import numpy as np

###################################################
# 設定・定義
###################################################
cfgpath = ""
csvtktpath = ""
sjistktpath = ""
impshpath = ""
delshpath = ""

# CSV書き込み項目
csvfmt = {
    "TicketNumber": 0,
    "Title": 1,
    "Folder": 2,
    "Priority": 3,
    "State": 4,
    "Type": 5,
    "Service": 6,
    "CustomerID": 7,
    "CustomerUser": 8,
    "Owner": 9,
    "Responsible": 10,
    "CreateTime": 11,
    "DynamicField_ITSMDueDate": 12,
    "DynamicField_ITSMImpact": 13,
    "DynamicField_IncidentType": 14,
    "DynamicField_TaiouKousuu": 15,
    "DynamicField_XITSMCloseDate": 16,
    "DynamicField_XITSMGeneralTextarea1": 17,
    "DynamicField_XITSMGeneralTextarea3": 18,
    "DynamicField_XITSMHostName": 19,
    "DynamicField_ProcessManagementProcessID": 20,
}
#################################################
# 関数
###################################################
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
            # 複合項目の場合
            clmval = ""
            for subkey, subval in val.items():
                clmval += "," if len(clmval) > 0 else ""
                clmval += subkey + ": "
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
# 項目値の重複および空文字を除き、項目値をキーとする辞書を作成
def uniquedic(keywds, recs):
    lst = []
    for keywd in keywds:
        lst = lst + [rec[keywd] for rec in recs]
    return {uniqrec:"" for uniqrec in np.unique(lst) if len(uniqrec) > 0}
# 項目マッピング用変換マスタに不足分を追加
def addmst(dstdic, mstkey, srcdic):
    dstdic.setdefault(mstkey, {})
    for key, val in srcdic.items():
        dstdic[mstkey].setdefault(key, val)
# 項目変換
def cnvval(dic, val):
   return dic[val] if len(dic) > 0 and len(val) > 0 else val 
# レコード変換
def cnvrec(rec):
    rec["TicketNumber"] = prjinf["TktNumPrefix"] + "-" + rec["TicketNumber"]
    rec["Folder"] = prjinf["Folder"]
    rec["Priority"] = cnvval(prjinf["mstPriority"], rec["Priority"])
    rec["State"] = cnvval(prjinf["mstState"], rec["State"])
    rec["Type"] = "インシデント"
    rec["Service"] = prjinf["Service"]
    rec["CustomerID"] = prjinf["CustomerID"]
    rec["CustomerUser"] = cnvval(prjinf["mstCustomerUser"], rec["CustomerUser"])
    rec["Owner"] = cnvval(prjinf["mstUser"], rec["Owner"])
    rec["Responsible"] = cnvval(prjinf["mstUser"], rec["Responsible"])
    rec["DynamicField_ITSMImpact"] = cnvval(prjinf["mstImpact"], rec["DynamicField_ITSMImpact"])
    rec["DynamicField_IncidentType"] = cnvval(prjinf["mstIncidentType"], rec["DynamicField_IncidentType"])
    for key,val in prjinf["ticketinfo"]["replaceclm"].items():
        rec[key] = re.sub(val["regexp"],val["repval"], rec[key])
    ### ここから暫定コード（書式指定のあるダイナミックフィールドは空文字にできない） ###
    # 状態（クローズのみ許可）
    rec["State"] = "クローズ"
    # 影響度（任意項目）
    if len(rec["DynamicField_ITSMImpact"]) == 0: rec["DynamicField_ITSMImpact"] = "3 normal"
    # クローズ日時（任意項目）
    if len(rec["DynamicField_XITSMCloseDate"]) == 0: rec["DynamicField_XITSMCloseDate"] = "9999/12/31 00:00:00"
    # 対応期限（任意項目）
    if len(rec["DynamicField_ITSMDueDate"]) == 0: rec["DynamicField_ITSMDueDate"] = "9999/12/31 00:00:00"
    # アクティビティID（テスト用）
    rec["DynamicField_ProcessManagementProcessID"] = "インシデント対応 (テスト)"
    return rec
###################################################
# メイン処理
###################################################
# 引数チェック
parser = argparse.ArgumentParser()
parser.add_argument("projectid")
args = parser.parse_args()
cfgpath = args.projectid + ".json"
csvtktpath = args.projectid + "_tickets.csv"
sjistktpath = args.projectid + "_tickets_sjis.csv"
impshpath = args.projectid + "_imp_all.sh"
delshpath = args.projectid + "_del_all.sh"

# 設定ファイル存在チェック
if not(os.path.isfile(cfgpath)):
    # 存在しない場合、テンプレートを作成して終了
    with open(cfgpath, encoding="utf-8", mode="w") as jsnfile:
        dic = {}
        dic["CustomerID"] = "利用者グループIDを指定して下さい"
        dic["Service"] = ""
        dic["TktNumPrefix"] = "チケットNoの前置詞（重複回避用）を指定して下さい"
        dic["Folder"] = ""
        dic["bookname"] = "管理台帳(excel)のファイル名を指定して下さい"
        dic["ticketinfo"] = {}
        dic["ticketinfo"]["sheetname"] = "管理台帳(excel)のシート名を指定して下さい"
        dic["ticketinfo"]["startrow"] = 0
        dic["ticketinfo"]["checkclm"] = ""
        dic["ticketinfo"]["format"] = csvfmt
        dic["ticketinfo"]["replaceclm"] = {}
        json.dump(dic, jsnfile, ensure_ascii=False, indent=4)
    print("設定ファイル（{}）が存在しない為、テンプレートを作成しました。\n".format(cfgpath))
    print("設定ファイルをメンテナンスの上、再実行してください\n")
    sys.exit(0)
# 設定ファイル読み込み
with open(cfgpath, encoding="utf-8", mode="r") as jsnfile:
    prjinf = json.load(jsnfile)
# EXCELファイル読み込み
exlfile = pd.read_excel(prjinf["bookname"], sheet_name=prjinf["ticketinfo"]["sheetname"], header=None)
# 有効行のみ、必要項目だけを抜き出す
exlrecs = [conv2csvfmt(shrinkclm(exlrec)) 
            for idx, exlrec in enumerate(exlfile.values) 
            if isvalidrec(idx, exlrec)]
# 優先度マッピング追加
addmst(prjinf, "mstPriority", uniquedic(["Priority"],exlrecs))
# 状態マッピング追加
addmst(prjinf, "mstState", uniquedic(["State"],exlrecs))
# 利用者マッピング追加
addmst(prjinf, "mstCustomerUser", uniquedic(["CustomerUser"],exlrecs))
# 運用者マッピング追加
addmst(prjinf, "mstUser", uniquedic(["Owner", "Responsible"],exlrecs))
# 影響度マッピング追加
addmst(prjinf, "mstImpact", uniquedic(["DynamicField_ITSMImpact"],exlrecs))
# インシデント分類マッピング追加
addmst(prjinf, "mstIncidentType", uniquedic(["DynamicField_IncidentType"],exlrecs))
# JSONファイル書き込み
with open(cfgpath, encoding="utf-8", mode="w") as jsnfile:
    json.dump(prjinf, jsnfile, ensure_ascii=False, indent=4)
    # jsnfile.write(json.dumps(prjinf, ensure_ascii=False, indent=4))
# インポートシェル書き込み
with open(impshpath, encoding="utf-8", newline='', mode='w') as impshfile:
    impshfile.write("#!/bin/bash\n")
    impshfile.write("perl /opt/FJSVbsmotrs/bin/otrs.ImportExport.pl -n 000006 -a import -i /root/import/{}\n".format(csvtktpath))
# CSVファイル、削除シェル書き込み
with open(csvtktpath, encoding="utf-8", newline='', mode='w') as csvtktfile, \
     open(delshpath, encoding="utf-8", newline='', mode='w') as delshfile:
    csvwriter = csv.DictWriter(
                            csvtktfile,
                            fieldnames=list(csvfmt.keys()), 
                            delimiter=',', 
                            quotechar='"',
                            lineterminator='\n', 
                            quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writeheader()
    delshfile.write("#!/bin/bash\n")
    for rec in exlrecs:
        recw = cnvrec(rec)
        csvwriter.writerow(recw)
        delshfile.write("perl /opt/FJSVbsmotrs/bin/otrs.TicketDelete.pl --TicketNumber {}\n".format(recw["TicketNumber"]))
# 確認用にSJIS変換
with open(csvtktpath, encoding="utf-8", newline='', mode='r') as csvtktfile, \
    open(sjistktpath, newline='', mode='w') as sjisfile:
    sjisfile.write(csvtktfile.read())