import argparse
import csv
import os
import DirObject

##################################
# メイン処理
##################################
def main():
    # 引数チェック
    parser = argparse.ArgumentParser()
    parser.add_argument("list_file")
    args = parser.parse_args()
    list_file = args.list_file
    list_file_out = list_file + ".out"
    # ディレクトリリスト読込
    rootDir = None
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
