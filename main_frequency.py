# -*- coding: utf-8 -*-
# @Time    : 2022/5/14 10:17 下午
# @Author  : ddy
# @FileName: main_frequency.py
# @github  : https://github.com/ddy-ddy

import json
import pandas as pd

# 读取json中的数据
info = []
words = []
with open("data/KaoYan_frequent.json", 'r') as f:
    for line in f.readlines():
        temp_info = eval(line)
        if temp_info["content"]["word"]["wordHead"]:
            words.append(temp_info["content"]["word"]["wordHead"])
            info.append(temp_info)
f.close()

# 提取word，解释，例子，用于导入到anki
'''
单词：word=info["content"]["word"]["wordHead"]

翻译：
    trans_pos=info["content"]["word"]["content"]["trans"][0]["pos"]
    trans=info["content"]["word"]["content"]["trans"][0]["tranCn"]
例句：
    sen_english=info["content"]["word"]["content"]["sentence"][0]["sContent"]
    sen_chinese=info["content"]["word"]["content"]["sentence"][0]["sCn"]
'''
all_info = []
example_sen = []

for temp in info:
    # anki正面
    word = temp["content"]["word"]["wordHead"]  # 单词

    # anki背面
    anki_info = {"trans": [], "example": []}

    # 翻译
    if temp["content"]["word"]["content"]["trans"]:
        temp_trans_info = temp["content"]["word"]["content"]["trans"]
        for item in temp_trans_info:
            temp_str = f"{item['pos']}.{item['tranCn']}"  # "词性.中文翻译"
            anki_info["trans"].append(temp_str)

    # 例句
    if "sentence" in temp["content"]["word"]["content"].keys():
        temp_exm_info = temp["content"]["word"]["content"]["sentence"]
        for item in temp_exm_info["sentences"]:
            anki_info["example"].append([item["sContent"], item["sCn"]])

    trans_str = ""
    for item in anki_info["trans"]:
        trans_str += item + "\n"

    exm_str = ""
    for _, item in enumerate(anki_info["example"]):
        str_sen = f"{_ + 1}. {item[0]}"
        str_tran = f"{item[1]}"
        exm_str += str_sen + "\n" + str_tran + "\n"

    if anki_info["example"] == []:
        word_sen = ""
        word_sen_trans = ""
    else:
        word_sen = anki_info["example"][0][0]
        word_sen_trans = anki_info["example"][0][1]
    # anki = trans_str +"\n"+ exm_str
    all_info.append([word, word_sen, word_sen_trans, trans_str, exm_str])
    # example_sen.append([anki_info["example"][0], anki_info["example"][1]])

this_info = all_info
data = pd.DataFrame({"word": [item[0] for item in this_info],
                     "word_sen": [item[1] for item in this_info],
                     "word_sen_trans": [item[2] for item in this_info],
                     "trans": [item[3] for item in this_info],
                     "example": [item[4] for item in this_info]})
data.to_csv("kaoyan_frequency_all.csv", index=False)
