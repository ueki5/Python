import requests
import json
import functools
# ディレクトリクラス
class DirObject:
    # コンストラクタ
    def __init__(self, fullPath, fileCount, fileSize):
        self.__init__
        self.fullPath = fullPath
        # ファイル数
        self.fileCount = fileCount
        self.totalCount = self.fileCount
        # 容量
        self.fileSize = fileSize
        self.totalSize = self.fileSize
        self.child = []
        self.hierarchy = splitDir(self.fullPath)
        self.depth = len(self.hierarchy)
    # 指定されたディレクトリが親かどうか判断
    def isParent(self, parDir):
        if self.fullPath.startswith(parDir.fullPath) \
           and len(self.fullPath) > len(parDir.fullPath):
            return True
        else:
            return False
    # 子ディレクトリ登録
    def addChild(self, child):
        # 総ファイル数を加算
        self.totalCount += child.totalCount
        # 総容量を加算
        self.totalSize += child.totalSize
        # 子供として登録
        self.child.append(child)
# ディレクトリ分割関数
def splitDir(dir_path):
    dir_list = []
    if (dir_path.startswith("\\\\")):
        # ￥￥から始まる場合、一旦除外して分割＆再結合
        dir_list = dir_path[2:].split("\\")
        dir_list[0] = "\\\\" + dir_list[0]
    else:
        dir_path.split("\\")
    return dir_list
# ディレクトリツリー走査ジェネレータ関数
def getDirGenerator(dirObject):
    yield dirObject
    for cldDir in dirObject.child:
        yield from getDirGenerator(cldDir)
    # raise StopIteration()


