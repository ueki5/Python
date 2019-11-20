import win32com.client

def pdf2text(fileName):
    text = ""
    doc = win32com.client.DispatchEx("AcroExch.Document")
    doc.AcroPDF.LoadFile(fileName)
    # text = ""
    # doc = win32com.client.Dispatch("AcroExch.FDFDoc")
    # doc.Visible = False # アプリで開かない
    # doc.DisplayAlerts = False # 警告OFF
    # try:
    #     doc_file = doc.EditDocument(fileName)
    #     for s in doc_file.Sentences:
    #         text += str.rstrip(str(s)) + "\n"
    #     doc_file.Close()
    # except AttributeError as ex:
    #     print("exception: {0}".format(ex))
    # finally:
    #     pass
    #     # doc.Quit()
    # return text
def word2text(fileName):
    text = ""
    doc = win32com.client.gencache.EnsureDispatch("Word.Application")
    doc.Visible = False # アプリで開かない
    doc.DisplayAlerts = False # 警告OFF
    try:
        doc_file = doc.Documents.Open(fileName, False, True) # 変換ダイアログ非表示、読み取り専用で開く
        for s in doc_file.Sentences:
            text += str.rstrip(str(s)) + "\n"
        doc_file.Close()
    finally:
        doc.Quit()
    return text
def main():
    # print(word2text('C:\opt\src\workspace\Python\ConvertToBox\word_file.docx'))
    print(pdf2text('C:\opt\src\workspace\Python\ConvertToBox\pdf_file_keyword.pdf'))
if __name__ == '__main__': main()
