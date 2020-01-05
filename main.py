import os
from list_extract_file import get_extract_file_list
from load_markdown import load_markdown
from make_card_html import make_card_simple
from html_to_pdf import html_to_pdf
from unite_pdf import pdf_merge

def main(root_path, html_debug=False):
    file_list = get_extract_file_list(root_path)
    card_list = []
    for item in file_list:
        if item == "root":
            continue
        parent_group_name = None
        for file_path in file_list[item]:
            parent_group_name = item.replace(file_list["root"], "", 1).replace("/", " > ")
            card_list.append(load_markdown(file_path, parent_group_name))
    # card_html_list = []
    pdf_merge_list = {}
    for card_chank in card_list:
        # if card_info["metadata"]["card_id"] != "ディレクトリ持ちのテストです_1":
        #     continue
        for card_info in card_chank:
            card_html = make_card_simple(card_info)
            file_path = root_path + card_info["metadata"]["card_id"]
            if card_info["metadata"]["group_id"] not in pdf_merge_list:
                pdf_merge_list[card_info["metadata"]["group_id"]] = []
            pdf_merge_list[card_info["metadata"]["group_id"]].append(file_path +  ".pdf")
            if html_debug == True:
                with open(file_path +  ".html", "wb") as file:
                    file.write(card_html.encode('utf-8'))
            html_to_pdf(card_html, file_path +  ".pdf")
    # print(pdf_merge_list)
    pdf_merge(root_path, pdf_merge_list)


if __name__ == "__main__":
    main("カード生成ツールマニュアル/")


# 全体の処理の流れ
#   設定ファイル読み込み
#   設定構築
#   カードファイル読み込み
#       順番にカード読み込み
#       カードと同じ名前のディレクトリが存在したらそれらを読み込む
