import PyPDF2
import os

# PdfFileMergerクラスのオブジェクトを生成
# append()メソッドでファイルを追加
# write()メソッドで書き出し
# close()で閉じる

def pdf_merge(root_path, merge_list, delete_file=True):
    for item in merge_list:
        merger = PyPDF2.PdfFileMerger()
        for pdf in merge_list[item]:
            merger.append(pdf)
            if delete_file == True:
               os.remove(pdf)
        merger.write(root_path + item + '.pdf')
        merger.close()
