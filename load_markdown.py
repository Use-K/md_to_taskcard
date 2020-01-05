import os
import markdown
import bs4
import datetime


# カード情報を作る関数
def make_card_data(card_group_name, page_count, file_update_time, header, content, parent_group_name=None, execution_deadline=None):
    temp_group_list = parent_group_name.split(">")
    temp_group_list.pop()
    temp_group_list.reverse()
    parent_group_id = None if len(temp_group_list) == 0 else temp_group_list[0]
    card_data = {
        "metadata": make_metadata(parent_group_id, card_group_name, card_group_name +"_"+str(page_count), file_update_time),
        "padding_data": make_padding_data(parent_group_name+card_group_name, file_update_time, page_count, execution_deadline),
        "content_data": make_content_data(header, content)
    }
    return card_data


def make_metadata(parent_group_id, group_id, card_id, file_update_time, config=None):
    metadata = {
        "parent_group_id":parent_group_id,
        "group_id": group_id,
        "card_id": card_id,
        "file_update_time":file_update_time,
        "config":config
    }
    return metadata

def make_padding_data(breadcrumbs, file_update_time, page_num, execution_deadline=None):
    padding_data = {
        "breadcrumbs": breadcrumbs,
        "file_update_time":file_update_time,
        "execution_deadline": execution_deadline,
        "page_num":page_num
    }
    return padding_data


def make_content_data(header, content):
    content_data = {
        "header": header,
        "content": content
    }
    return content_data


# ファイル一つを読み込む時の処理
def load_markdown_simple(markdown_text, file_update_time, parent_group_name=None, execution_deadline=None, config=None):
    md = markdown.Markdown()
    parsed_html = md.convert(markdown_text)
    bs_html = bs4.BeautifulSoup(parsed_html, "html.parser")
    h2_flag = 0
    card_data_list = []
    # 取得するメタデータの定義
    page_count = 0
    card_group_name = None
    execution_deadline = execution_deadline
    header = None
    content = []

    parent_group_name = "" if parent_group_name is None else parent_group_name
    for html in bs_html:
        if html.name is None:
            continue
        chk_flag = False
        for check_text in ["実行期限", "期限", "締め切り", "締切", "〆切", "〆切り"]:
            if check_text in str(html.text):
                execution_deadline = html.text
                chk_flag = True
        if chk_flag is True:
            continue
        if html.name == "h1":
            card_group_name = html.text
        # h2が出てきた時の処理
        if html.name == "h2":
            # 初めて出てきたら
            #   最初のページを作る
            if h2_flag == 0:
                h2_flag = 1
                # first_page_header = bs_html.new_tag("h2")
                # first_page_header.string = card_group_name
                # header = str(first_page_header).replace("\n","")
            card_data = make_card_data(
                card_group_name,
                page_count,
                file_update_time,
                header,
                "".join(content),
                parent_group_name=parent_group_name,
                execution_deadline=execution_deadline
            )
            card_data_list.append(card_data)
            header = html.text
            content = []
            execution_deadline = None
            page_count += 1
            continue
        content.append(str(html).replace("\n",""))
    card_data = make_card_data(
        card_group_name,
        page_count,
        file_update_time,
        header,
        "".join(content),
        parent_group_name=parent_group_name,
        execution_deadline=execution_deadline)
    card_data_list.append(card_data)
    return card_data_list

def load_markdown(file_path, parent_group_name):
    file_markdown = open(file_path)
    file_text = file_markdown.read()
    statinfo = os.stat(file_path)
    file_update_time = datetime.datetime.fromtimestamp(statinfo.st_mtime, datetime.timezone(datetime.timedelta(hours=9)))
    file_update_time = file_update_time.strftime("%Y-%m-%d %H:%M")
    return load_markdown_simple(file_text, file_update_time, parent_group_name=parent_group_name)

if __name__ == "__main__":
    path = "test/test.md"
    file_markdown = open(path)
    file_text = file_markdown.read()
    statinfo = os.stat(path)
    file_update_time = datetime.datetime.fromtimestamp(statinfo.st_mtime, datetime.timezone(datetime.timedelta(hours=9)))
    file_update_time = file_update_time.strftime("%Y-%m-%d %H:%M")
    load_markdown_simple(file_text, file_update_time)