import argparse
import csv
import os
import DirObject

##################################
# ディレクトリチェック関数
##################################
def dirCheck(dirPath):
    fileList = []
    dirList = []
    objs = os.listdir(dirPath)
    for obj in objs:
        if os.path.isfile(os.path.join(dirPath, obj)):
            
##################################
# メイン処理
##################################
def main():
    # 引数チェック
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path")
    args = parser.parse_args()
    dir_path = args.dir_path
    # ディレクトリリスト読込
    dirCheck(dir_path)
    curStack = []
    with open(list_file,newline="") as infile:
        reader = csv.reader(infile)
        for row in reader:
            # 読み込み行をディレクトリクラスへ変換
            fullPath = row[1]
            fileCount = int(row[3])
            fileSize = int(row[4])
            curDir = DirObject.DirObject(fullPath, fileCount, fileSize)
            # 処理スタック中の子ディレクトリを抽出
            cldDirs = [cldDir for cldDir in curStack if cldDir.isParent(curDir) == True]
            for cldDir in cldDirs:
                # 子ディレクトリを取り込む
                curDir.addChild(cldDir)
                # 子ディレクトリを処理スタックから削除する
                curStack.remove(cldDir)
            # 自分を処理スタックに入れる
            curStack.append(curDir)
    # 最後のディレクトリをルートとして登録
    rootDir = curDir
    with open(list_file_out, encoding="cp932",mode="w",newline="") as outfile:
        writer = csv.writer(outfile)
        for dirobj in DirObject.getDirGenerator(rootDir):
            writer.writerow([dirobj.fullPath, dirobj.depth, dirobj.totalCount, dirobj.totalSize, dirobj.fileCount, dirobj.fileSize])
if __name__ == "__main__":
    main()
