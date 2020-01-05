import copy

# 一つ一つのカードに対して処理を実施
CARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8" />
        <title>{card_id}</title>
        <style>
            html {{
                height: 100%;
                font-size: 10pt;
            }}
            @page {{
                size: 127mm 89mm;
                margin: 0mm 3mm;
                font-family:'源ノ角ゴシック Regular','源ノ角ゴシック';
            }}

            body,
            #wrapper {{
                display: flex;
                flex-direction: column;
                height: 100%;
                
            }}

            header {{

                height: 10%;
                border-bottom: solid 1px #000000;
                padding-bottom: 3mm;
            }}

            header > #file_update_time {{
                text-align: right;
                font-size: 80%;
            }}

            header > #execution_deadline {{
                text-align: right;
                color: red;
                font-weight: bold;
            }}

            main {{
                height: 80%;
            }}

            main > #breadcrumbs {{
                padding-top: 3mm;
                font-size: 70%;
            }}

            footer {{
                height: 10%;
                margin-top: auto;
                text-align: right;
                border-top: solid 1px #000000;
                padding-top: 1mm;
                padding-bottom: 2mm;
            }}

            footer > #page_count {{
                font-size: 10pt
            }}

            h1,h2 {{
                margin-block-start: 1mm;
                margin-top: 1mm;
                margin-block-end: 2mm;
                margin-bottom: 2mm;
            }}
            p {{
                line-height: 1.35em;
                margin-block-start: 1mm;
                margin-top: 1mm;
                margin-block-end: 1mm;
                margin-bottom: 1mm;
                padding-left: 1em;
            }}

            ul {{
                font-size: 90%;
                margin-top: 0mm;
                margin-block-start: 0mm;
                padding-inline-start: 0mm;
                padding-top: 0mm;
                padding-left: 2em;
            }}

            main > ul {{
                margin-top: 2mm;
                margin-block-start: 2mm;
                padding-inline-start: 0mm;
                padding-top: 0mm;
                padding-left: 2em;
            }}
        </style>
    </head>
    <body>
        <div id="wrapper">
            <header>
                <div id="file_update_time">カード更新日時：{file_update_time}</div>
                {execution_deadline}
            </header>
            <main>
                <div id="breadcrumbs">{breadcrumbs}</div>
                {header}
                {content}
            </main>
            <footer>
                <div id="page_count">{page_num}</div>
            </footer>
        </div>
    </body>
</html>
'''


def make_card_simple(card_data):
    card_data["metadata"]["card_id"]
    card_html = copy.copy(CARD_TEMPLATE)
    card_html = card_html.format(
        card_id=card_data["metadata"]["card_id"],
        breadcrumbs=card_data["padding_data"]["breadcrumbs"],
        file_update_time=card_data["padding_data"]["file_update_time"],
        execution_deadline="" if card_data["padding_data"]["execution_deadline"] is None else '<div id="execution_deadline">' + card_data["padding_data"]["execution_deadline"] + '</div>',
        header="" if card_data["content_data"]["header"] is None else "<h2>" + card_data["content_data"]["header"] + "</h2>",
        content=card_data["content_data"]["content"],
        page_num=card_data["padding_data"]["page_num"]
    )
    return card_html

if __name__ == "__main__":
    pass