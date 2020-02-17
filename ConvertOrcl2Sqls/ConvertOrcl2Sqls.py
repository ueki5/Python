import argparse
import pyodbc
import pandas as pd

class DbType(Enum):
    SQLSERVER = 0
    ORACLE = 1
##################################
# ユーティリティ
##################################
def ExecuteSQL(sql, dbType):
    con = pyodbc.connect(GetConStr(dbType))
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def ReadQuery(sql, dbType):
    con = pyodbc.connect(GetConStr(dbType))
    df = pd.io.sql.read_sql(sql,con)
    con.close()
    return(df)
def GetConStr(dbType):
    conStr = r''
    if dbType == DbType.SQLSERVER:
        conStr = r'DRIVER={SQL Server};SERVER=localhost\SQLExpress;DATABASE=APM;UID=apm;PWD=apmPassword!;'
    elif dbType == DbType.ORACLE:
        conStr = r''
    return conStr
##################################
# メイン処理
##################################
def main():
    # 選択クエリを発行
    editSql = "SELECT * FROM dbo.T_RSCINF"
    df = lib.PyUtils.ReadQuery(editSql, DbType.SQLSERVER)  # SELECT文の発行
    for line in df.values:
        print(','.join(line))        
if __name__ == "__main__":
    main()
