# -*- coding: utf-8 -*-
"""
@time: 2020/3/12
@author: flx
"""

import pandas as pd
import jieba
import jieba.analyse
from collections import Counter
import json
import logging

#  数据预处理部分，训练模型准备：把训练数据加载并分词，查看词权重
#  加载jason格式训练数据，转化为字典，然后转化为dataframe
jieba.setLogLevel(logging.INFO)

def load(file):
    """
    输入文件名，加载数据
    :param file:文件名
    :return:dataframe表格
    """
    try:
        n = 0
        f11 = open(file, 'r', encoding='utf-8')
        lines = f11.readlines()
        for line in lines:
            line1 = line.replace('null', '"0"')
            line2 = eval(line1)
            if n == 0:
                df0 = pd.DataFrame([line2])
            else:
                df0 = df0.append(line2, ignore_index=True)
            n += 1
        f11.close()
        return df0
    except:
        print('输入数据集有误，检查是否为{}形式的jason或字符串')

#  把样本经过分词停用词处理后，转化成列表，每个元素为一条样本的词，可用于将来的转化tfdif向量
#  以前输入字符串格式菜单+菜单内容时用，后面用fastapi，输入的是菜单内容字符串


def text_croupslist(df1, stopwords_path):
    f2 = open(stopwords_path, 'r', encoding='utf-8')
    stop_lines = f2.readlines()
    stopwords = [i.strip() for i in stop_lines]
    f2.close()
    croups = []
    for i in df1.index:
        jieba.suggest_freq(('人民', '广场'), True)
        segs = jieba.lcut(
            df1.at[i, 'a'] + df1.at[i, 'n1'] + df1.at[i, 'n2'] + df1.at[i, 'n3']
            + df1.at[i, 'n4'])
        over_words = ''
        for seg in segs:
            if seg not in stopwords and seg != ' ' and not seg.isdigit():
                over_words = over_words + seg + ' '
        croups.append(over_words.strip())
    return croups
#  croup为列表


def str_croupslist(strings, stopwords_path):
    f3 = open(stopwords_path, 'r', encoding='utf-8')
    stop_lines = f3.readlines()
    stopwords = [i.strip() for i in stop_lines]
    f3.close()
    croups = []
    jieba.suggest_freq(('人民', '广场'), True)
    segs = jieba.lcut(strings)
    over_words = ''
    for seg in segs:
        if seg not in stopwords and seg != ' ' and not seg.isdigit():
            over_words = over_words + seg + ' '
    croups.append(over_words.strip())
    return croups

# 数据预处理：文本-分词-权重表示
#  提取关键词，用tfdif方式：


def list_tfdif(croups_list):
    textall = ''
    for i in croups_list:
        textall = textall + i
    li_tfdif = jieba.analyse.extract_tags(textall, topK=270, withWeight=True, allowPOS=())
    return li_tfdif
#  提取关键词，用tf词频方式：


def list_tf(croups_list):
    #  每个词列表
    textallseg = []
    for i in croups_list:
        line = i.split(' ')
        for j in line:
            textallseg.append(j)
    data = dict(Counter(textallseg))
    li_tf = sorted(data.items(), key=lambda x: x[1], reverse=True)
    return li_tf


#  算法部分：
#  基于规则：把每条样本转化为词，然后计算所有词（不重复）的相加权重值
#  算法准备:把输入的一条字符串文本，转化为以词为单位的列表，并做去重处理
def input_df(text):

    """
    输入字符串（json一条）转表格
    :return:dataframe表格
    """
    text_in = text.replace('null', '"0"')
    text_in = eval(text_in)
    df_in = pd.DataFrame([text_in])
    return df_in


def list_words(text_list1):
    """
    大列表转化成单词列表
    """
    text_list1[0].split(' ')
    return text_list1[0].split(' ')


def text_to_model(strings, stopwords_path):
    #  text_in_df = input_df(text)#字符串转表格
    # 表格经过分词停用词转化为列表
    text_list = str_croupslist(strings, stopwords_path)
    # 大列表转单词列表
    text_list_words = list_words(text_list)
    # 列表转集合，去重
    text_set_words = set(text_list_words)
    return text_set_words


def ruler(text, stopwords_path):
    text_in = text_to_model(text, stopwords_path)
    value = 0
    for i in text_in:
        if i in norm_tfdif_dic:
            value = norm_tfdif_dic[i] + value
    return value


def accthr(thr, stopwords_path):
    tp = 0
    p_num = 0
    tn = 0
    n_num = 0
    for line in lines_pos:
        p_num = p_num + 1
        if ruler(line, stopwords_path) >= thr:
            tp = tp + 1
    for line in lines_neg:
        n_num = n_num + 1
        if ruler(line, stopwords_path) < thr:
            tn = tn + 1
    fn = p_num - tp
    fp = n_num - tn
    acc = (tp + tn)/(tp + fn + tn + fp)
    pre = tp/(tp + fp)
    recall = tp/(tp + fn)
    ff1 = 2*pre*recall/(pre + recall)
    return 'acc:', acc, 'pre:', pre, 'recall:', recall, 'F1:', ff1


if __name__ == '__main__':
    # 把侵权数据集加载进来成df1格式，然后把表格所有词做成列表
    filepos = './data/pos.txt'
    filestopwords = './data/stop_words.txt'
    df1 = load(filepos)
    croups_list_pos = text_croupslist(df1, filestopwords)
    #  侵权词权重，以此判断,所有词权重相加值
    norm_tfdif = list_tfdif(croups_list_pos)
    norm_tfdif_dic = dict(norm_tfdif)
    res2 = json.dumps(norm_tfdif_dic)
    with open('tfdif.json', 'w', encoding='utf-8') as f:  # 打开文件
        f.write(res2)
    f = open('./data/pos.txt', 'r', encoding='utf-8')
    lines_pos = f.readlines()
    f.close()
    f = open('./data/neg.txt', 'r', encoding='utf-8')
    lines_neg = f.readlines()
    f.close()
    print(accthr(0.01, filestopwords))
