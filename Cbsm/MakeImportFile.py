import datetime
import json
import csv
import pandas as pd
import numpy as np

###################################################
# 設定・定義
###################################################
exlpath = 'オフサイト契約依頼事項.xlsx'
jsnpath = 'projectinf.json'
csvpath = 'imptickets.csv'
startrow = 4 # 有効行開始位置
checkclm = "Title" # 有効行判定項目名

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
    "CreateUser": 12,
    "ChangeTime": 13,
    "DynamicField_ITSMDueDate": 14,
    "DynamicField_ITSMImpact": 15,
    "DynamicField_IncidentType": 16,
    "DynamicField_TaiouKousuu": 17,
    "DynamicField_XITSMCloseDate": 18,
    "DynamicField_XITSMGeneralTextarea1": 19,
    "DynamicField_XITSMGeneralTextarea3": 20,
}
#################################################
# 関数
###################################################
# 値の有効判定
def isvalidval(n):
    return (isinstance(n, (str, datetime.date))
             or (n is not None and not(np.isnan(n))))
# 行の有効判定
def isvalidrec(idx, lst):
    return idx >= startrow and isvalidval(lst[prjinf["exlfmt"][checkclm]])
# 全項目(のリストから、必要項目だけを辞書型で抜き出す
def shrinkclm(lst):
    return {key:lst[idx] for key,idx in prjinf["exlfmt"].items()}
# 書き出し用レコード作成
def conv2csvfmt(srcdic):
    dstdic = {}
    # 読み込み項目転記
    for key,val in srcdic.items():
        dstdic[key] = (str(val) if isvalidval(val) else 
                        "{0:%Y-%m-%d %H:%M:%S}".format(val) if isinstance(val, datetime.date) 
                        else "")
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
    rec["Type"] = "3" # 「3:インシデント」固定
    rec["Service"] = prjinf["Service"]
    rec["CustomerID"] = prjinf["CustomerID"]
    rec["CustomerUser"] = cnvval(prjinf["mstCustomerUser"], rec["CustomerUser"])
    rec["Owner"] = cnvval(prjinf["mstUser"], rec["Owner"])
    rec["Responsible"] = cnvval(prjinf["mstUser"], rec["Responsible"])
    rec["DynamicField_ITSMImpact"] = cnvval(prjinf["mstImpact"], rec["DynamicField_ITSMImpact"])
    # # 必須項目ではない「影響度」が、なぜか空文字にできない
    # if len(rec["DynamicField_ITSMImpact"]) == 0:
    #     rec["DynamicField_ITSMImpact"] = "3 normal"
    rec["DynamicField_IncidentType"] = cnvval(prjinf["mstIncidentType"], rec["DynamicField_IncidentType"])
    return rec
###################################################
# メイン処理
###################################################
# 設定ファイル読み込み
with open(jsnpath, encoding="utf-8", mode="r") as jsnfile:
    prjinf = json.load(jsnfile)
# EXCELファイル読み込み
exlfile = pd.read_excel(exlpath, sheet_name="依頼事項一覧")
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
with open(jsnpath, encoding="utf-8", mode="w") as jsnfile:
    json.dump(prjinf, jsnfile, ensure_ascii=False, indent=4)
    # jsnfile.write(json.dumps(prjinf, ensure_ascii=False, indent=4))
# CSVファイル書き込み
with open(csvpath, encoding="utf-8", newline='', mode='w') as csvfile:
    csvwriter = csv.DictWriter(
                            csvfile,
                            fieldnames=list(csvfmt.keys()), 
                            delimiter=',', 
                            quotechar='"',
                            lineterminator='\n', 
                            quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writeheader()
    for rec in exlrecs:
        csvwriter.writerow(cnvrec(rec))
