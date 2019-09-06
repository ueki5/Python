import json
import csv
import pandas as pd
import numpy as np

###################################################
# 設定・定義
###################################################
exlpath = 'オフサイト契約依頼事項.xlsx'
csvpath = 'imp_tickets.csv'
startrow = 4 # 有効行開始位置
checkclm = "Title" # 有効行判定項目名

# EXCEL読み取り項目
inrec = {
    "TicketNumber":1,
    "Title":2,
    "Priority":9,
    "State":17,
    "CustomerID":0,
    "CustomerUser":4,
    "Owner":16,
    "Responsible":16,
    "DynamicField_ITSMDueDate":11,
    "DynamicField_TaiouKousuu":13,
    "DynamicField_XITSMCloseDate":18,
    "DynamicField_XITSMGeneralTextarea1":2,
    "DynamicField_XITSMGeneralTextarea3":10,
}
# CSV書き込み項目
outrec = {
    "TicketNumber":0,
    "Title":1,
    "Folder":2,
    "Priority":3,
    "State":4,
    "Type":5,
    "Service":6,
    "CustomerID":7,
    "CustomerUser":8,
    "Owner":9,
    "Responsible":10,
    "CreateTime":11,
    "CreateUser":12,
    "ChangeTime":13,
    "DynamicField_ITSMDueDate":14,
    "DynamicField_ITSMImpact":15,
    "DynamicField_IncidentType":16,
    "DynamicField_TaiouKousuu":17,
    "DynamicField_XITSMCloseDate":18,
    "DynamicField_XITSMGeneralTextarea1":19,
    "DynamicField_XITSMGeneralTextarea3":20,
}
#################################################
# 関数
###################################################
# 値の有効判定
def isvalidval(n):
    return isinstance(n,str) or not(np.isnan(n))
# 行の有効判定
def isvalidrec(idx, lst):
    return idx >= startrow and isvalidval(lst[inrec[checkclm]])
# EXCELの全項目(のリストから、必要項目だけを辞書型で抜き出す
def exl2csv(lst):
    return {key:lst[idx] for key,idx in inrec.items()}

###################################################
# メイン処理
###################################################
# EXCELファイル読み込み
exlfile = pd.read_excel(exlpath, sheet_name="依頼事項一覧")
# 有効行のみ、必要項目だけを抜き出す
partrec = [exl2csv(allrec) 
            for idx, allrec in enumerate(exlfile.values) 
            if isvalidrec(idx, allrec)]
# CSVファイル書き込み
with open(csvpath, encoding='utf-8', newline='', mode='w') as csvfile:
    csvwriter = csv.DictWriter(
                            csvfile, 
                            fieldnames=list(inrec.keys()), 
                            delimiter=',', 
                            quotechar='"', 
                            quoting=csv.QUOTE_NONNUMERIC)
    for rec in partrec:
        # print(rec)
        csvwriter.writerow(rec)