# -*- coding: utf-8 -*-
"""
@time: 2020/3/12
@author: flx
"""
from .opt import *
import json
import os


def get_file_path():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    company_dir_path = os.path.join(BASE_DIR, 'optiz/data/stop_words.txt')
    return company_dir_path


filestopwords = get_file_path()
f = open('tfdif.json', encoding="utf-8")
tfdifdic = json.load(f)
f.close()


def ruler(text, stopwords_path):
    text_in = text_to_model(text, stopwords_path)
    value = 0
    for i in text_in:
        if i in tfdifdic:
            value = tfdifdic[i] + value
    return value


def pre(text):
    try:
        y = 0
        value = ruler(text, filestopwords)
        if value >= 0.01:
            y = 1
        else:
            y = 0
        return y
    except Exception as r:
        return r, '数据格式错误，请查看'


if __name__ == '__main__':
    pre('{"a": "人民", "n1": "电影", "n2": "经过", "n3": "免费", "n4": ""}')
