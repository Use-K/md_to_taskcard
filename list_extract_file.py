import os
import glob


def get_file_dir_list(root_dir):
    file_list = [p for p in glob.glob(root_dir +'*') if os.path.isfile(p) and "md" in p]
    file_name_list = [p.replace(root_dir, "").replace(".md", "") for p in glob.glob(root_dir +'/*') if os.path.isfile(p) and "md" in p]
    dir_list = []
    for dir_str in glob.glob(root_dir + "**/"):
        if dir_str.replace(root_dir, "").replace("/","") in file_name_list:
            dir_list.append(dir_str)
    return file_list, dir_list

def get_extract_file_list(root_dir):
    dir_list = [root_dir]
    file_list = {"root": root_dir}
    while 1==1:
        for dir_str in dir_list:
            extracted_file_list, extracted_dir_list = get_file_dir_list(dir_str)
            file_list[dir_str] = extracted_file_list
            dir_list.extend(extracted_dir_list)
            dir_list.remove(dir_str)
        if len(dir_list) == 0:
            break
    return file_list


# 単純なリスト取得
# mdファイルとディレクトリファイルの弁別
# ディレクトリのうち、ファイル名が存在するものだけ取得
if __name__ == "__main__":
    dir_file_list = get_extract_file_list("test/")
    for item in dir_file_list:
        if item == "root":
            continue
        print(item.replace(dir_file_list["root"], "",1).replace("/", ">"))