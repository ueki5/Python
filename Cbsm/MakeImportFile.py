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
    "DynamicField_ProjectSpecific": 19
}
#################################################
# 関数
###################################################
# 26進変換
n_ary = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z"
]
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
                # カンマの後にスペースが必要なので、注意（そうしないと画面上で複数項目に区切られません）
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
    # 影響度（任意項目）
    if len(rec["DynamicField_ITSMImpact"]) == 0: rec["DynamicField_ITSMImpact"] = "3 normal"
    # クローズ日時（任意項目）
    if len(rec["DynamicField_XITSMCloseDate"]) == 0: rec["DynamicField_XITSMCloseDate"] = "9999/12/31 00:00:00"
    # 対応期限（任意項目）
    if len(rec["DynamicField_ITSMDueDate"]) == 0: rec["DynamicField_ITSMDueDate"] = "9999/12/31 00:00:00"
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
    # 存在しない場合、メッセージ表示して終了
    print("設定ファイル（{}）が存在しない為、終了します。\n".format(cfgpath))
    sys.exit(1)
# 設定ファイル読み込み
with open(cfgpath, encoding="utf-8", mode="r") as jsnfile:
    prjinf = json.load(jsnfile)
#####################################################
# 機械にわかりやすい用、行指定、列指定をExcel基準から変換
#####################################################
# 開始行
prjinf["ticketinfo"]["startrow"] = rowToIdx(prjinf["ticketinfo"]["startrow"])
# コラム（列）位置
for key, val in prjinf["ticketinfo"]["format"].items():
    if key == "DynamicField_ProjectSpecific":
        # 複数項目を保持している為、子要素に対して変換を行う
        for key2, val2 in prjinf["ticketinfo"]["format"]["DynamicField_ProjectSpecific"].items():
            prjinf["ticketinfo"]["format"]["DynamicField_ProjectSpecific"][key2] = a1ToIdx(val2)
    else:
        prjinf["ticketinfo"]["format"][key] = a1ToIdx(val)
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
#####################################################
# 人間にわかりやすいよう、行指定、列指定をExcel基準に変換
#####################################################
# 開始行
prjinf["ticketinfo"]["startrow"] = idxToRow(prjinf["ticketinfo"]["startrow"])
# コラム（列）位置
for key, val in prjinf["ticketinfo"]["format"].items():
    if key == "DynamicField_ProjectSpecific":
        # 複数項目を保持している為、子要素に対して変換を行う
        for key2, val2 in prjinf["ticketinfo"]["format"]["DynamicField_ProjectSpecific"].items():
            prjinf["ticketinfo"]["format"]["DynamicField_ProjectSpecific"][key2] = idxToA1(val2)
    else:
        prjinf["ticketinfo"]["format"][key] = idxToA1(val)
# JSONファイル書き込み
with open(cfgpath, encoding="utf-8", mode="w") as jsnfile:
    json.dump(prjinf, jsnfile, ensure_ascii=False, indent=4)
    # jsnfile.write(json.dumps(prjinf, ensure_ascii=False, indent=4))
# インポートシェル書き込み
with open(impshpath, encoding="utf-8", newline='', mode='w') as impshfile:
    impshfile.write("#!/bin/bash\n")
    impshfile.write("perl /opt/FJSVbsmotrs/bin/otrs.ImportExport.pl -n 000005 -a import -i /root/import/{}\n".format(csvtktpath))
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
print("インポート用のCSV（{}）が作成されました。\n".format(csvtktpath))
# 確認用にSJIS変換
try:
    with open(csvtktpath, encoding="utf-8", newline='', mode='r') as csvtktfile, \
        open(sjistktpath, newline='', mode='w') as sjisfile:
        sjisfile.write(csvtktfile.read())
except:
    # 存在しない場合、メッセージ表示して終了
    print("確認用のCSV（{}）の作成に失敗しました。\n".format(sjistktpath))
else:
    print("確認用のCSV（{}）が作成されました。\n".format(sjistktpath))
