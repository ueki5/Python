import os
import argparse
import pathlib
import glob
import re
# pdfminer(pip install pdfminer3k)
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfparser import PDFDocument
# olefile(pip install olefile)
import olefile
import win32com.client

##################################
# 関数
##################################
# pdfファイル
def cnvPdf(srcPath, dstPath):
    # fp = open(srcPath, 'wb')
    # parser = PDFParser(fp)
    # doc = PDFDocument(parser)
    # parser.set_document(doc)
    # doc.set_parser(parser)
    # print(doc.info[0]["Category"])
    # print(doc.info[0]["Keywords"])
    return True
# wordファイル
def cnvWord(srcPath, dstPath):
    # doc = win32com.client.gencache.EnsureDispatch("Word.Application")
    # doc.Visible = False # アプリで開かない
    # doc.DisplayAlerts = False # 警告OFF
    # try:
    #     doc_file = doc.Documents.Open(srcPath, False, True) # 変換ダイアログ非表示、読み取り専用で開く
    #     for s in doc_file.Sentences:
    #         pass
    #     doc_file.Close()
    # finally:
    #     doc.Quit()
    return True
def cnvExcel(srcPath, dstPath):
    return True
def cnvPPoint(srcPath, dstPath):
    return True
def cnvText(srcPath, dstPath):
    return True
def cnvOther(srcPath, dstPath):
    return True
def isOutlookData(suffix):
    if suffix == ".pst":
        return True
    else:
        return False
def isExecutable(suffix):
    if suffix == ".bat" or \
       suffix == ".cmd" or \
       suffix == ".com" or \
       suffix == ".cpl" or \
       suffix == ".desklink" or \
       suffix == ".exe" or \
       suffix == ".hta" or \
       suffix == ".lnk" or \
       suffix == ".mapmai" or \
       suffix == ".pif" or \
       suffix == ".scr" or \
       suffix == ".shs" or \
       suffix == ".url" or \
       suffix == ".vbs":
        return True
    else:
        return False
def cnvFile(srcPath, dstDir, dstPath, suffix):
    if os.path.exists(dstDir) == False:
        os.makedirs(dstDir)
    if suffix == ".pdf":
        # PDFファイル
        pass
    if suffix == ".xls" or suffix == ".xlsx":
        # Excelファイル
        ret = cnvWord(srcPath, dstPath)
    elif suffix == ".doc" or suffix == ".docx":
        # Wordファイル
        ret = cnvWord(srcPath, dstPath)
    elif suffix == ".ppt" or suffix == ".pptx":
        # PowerPointファイル
        ret = cnvPPoint(srcPath, dstPath)
    elif suffix == ".txt":
        # テキストファイル
        ret = cnvText(srcPath, dstPath)
    elif isOutlookData(suffix):
        # アウトルックデータファイル
        ret = False
    elif isExecutable(suffix):
        # 実行可能ファイル
        ret = False
    else:
        # その他のファイル
        ret = cnvOther(srcPath, dstPath)
    return ret
def moveFile(srcPath, dstPath):
    return True

##################################
# メイン処理
##################################
def main():
# 引数チェック
    parser = argparse.ArgumentParser()
    parser.add_argument("src_dir")
    parser.add_argument("dst_dir")
    parser.add_argument("bak_dir")
    args = parser.parse_args()
    src_dir = args.src_dir
    dst_dir = args.dst_dir
    bak_dir = args.bak_dir
    pathItr = pathlib.Path(args.src_dir).resolve()
    for p in ([p for p in pathItr.glob('**/*') if p.is_file()]):
        # 移行元
        srcDir = str(p.parent)
        srcPath = str(p)
        # 移行先
        dstDir = srcDir.replace(src_dir, dst_dir)
        dstPath = srcPath.replace(src_dir, dst_dir)
        suffix = p.suffix
        # 移行
        print("{}".format(srcPath))
        if cnvFile(srcPath, dstDir, dstPath, suffix):
            # 移行が成功したら、ファイルを移動
            moveFile(src_dir, bak_dir)
if __name__ == "__main__":
    main()
