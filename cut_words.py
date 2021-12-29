#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Created 2021/9/18
@author:Jane
"""

import os
import time

import jieba
import jieba.posseg as pseg
import pandas as pd
from path import keyword,datapath,itempath

#dictpath = os.path.join(itempath,'dict')
#这里是标题.csv
df=pd.read_csv(os.path.join(datapath,'reviews.csv'), header=0, error_bad_lines=False).astype(str)

#在读数之后自定义标题
#columns_name=['ouid','weiboid','time','nickname','id','t_id','reviews']
#[attitudes,comments,created,id,name,reposts,sex,text,text_Length,topic,user_id]
columns_name=['id','name','created','text']
df.columns=columns_name
#print(df.head(3))
# _ret = []
# data = pd.DataFrame(_ret,columns_name = ['ouid','reviews'])
#

# DataFrame(df['review_split'].astype(str))
# DataFrame(df['review_pos'].astype(str))
# DataFrame(df['review_split_pos'].astype(str))

df['review_split']='new' #创建分词结果列：review_split
df['review_pos']='new' #创建词性标注列：review_pos
df['review_split_pos']='new' #创建分词结果/词性标注列：review_split_pos

#   调用jieba分词包进行分词
def jieba_cut(review):
    review_dict = dict(pseg.cut(review))
    return review_dict

# 创建停用词列表
def stopwordslist(stopwords_path):
    stopwords = [line.strip() for line in open(stopwords_path,encoding='UTF-8').readlines()]
    return stopwords

# 获取分词结果、词性标注结果、分词结果/分词标注结果的字符串
def get_fenciresult_cixin(review_dict_afterfilter):
    keys = list(review_dict_afterfilter.keys()) #获取字典中的key
    values = list(review_dict_afterfilter.values())
    review_split=" ".join(keys)
    review_pos=" ".join(values)
    review_split_pos_list = []
    for j in range(0,len(keys)):
        review_split_pos_list.append(keys[j]+" "+values[j])
    review_split_pos=",".join(review_split_pos_list)
    return review_split,review_pos,review_split_pos


stopwordslist=stopwordslist(os.path.join(itempath,'dict','stopword.txt'))
#stopwords = {}.fromkeys([line.rstrip() for line in open('Stopword.txt', encoding='utf-8')])

#review="刚刚才离开酒店，这是一次非常愉快满意住宿体验。酒店地理位置对游客来说相当好，离西湖不行不到十分钟，离地铁口就几百米，周围是繁华商业中心，吃饭非常方便。酒店外观虽然有些年头，但里面装修一点不过时，我是一个对卫生要求高的，对比很满意，屋里有消毒柜可以消毒杯子，每天都有送两个苹果。三楼还有自助洗衣，住客是免费的，一切都干干净净，服务也很贴心，在这寒冷的冬天，住这里很温暖很温馨"
#分词与词性标注
def fenci_and_pos(review):
    #01 调用jieba的pseg同时进行分词与词性标注，返回一个字典 d = {key1 : value1, key2 : value2 }
    review_dict= jieba_cut(review)
    # print(review_dict)
    # 02 停用词过滤
    review_dict_afterfilter = {}
    for key, value in review_dict.items():
        if key not in stopwordslist:
            review_dict_afterfilter[key] = value
        else:
            pass
    # print(review_dict_afterfilter)
    #03 获取分词结果、词性标注结果、分词+词性结果
    review_split, review_pos,review_split_pos = get_fenciresult_cixin(review_dict_afterfilter)
    return review_split,review_pos,review_split_pos

def fenci_pos_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    return elapsed_mins, elapsed_secs

# fenci_and_pos(review)
jieba.load_userdict(os.path.join(itempath,'dict','jiebadict_baidu.txt'))
jieba.load_userdict(os.path.join(itempath,'dict','dict_baidu.txt'))
jieba.load_userdict(os.path.join(itempath,'dict','dict_pangu.txt'))
jieba.load_userdict(os.path.join(itempath,'dict','dict_sougou.txt'))
jieba.load_userdict(os.path.join(itempath,'dict','dict_tencent.txt'))
jieba.load_userdict(os.path.join(itempath,'dict','user_dict.txt'))
#使用用户自定义的词典

start_time = time.time()
review_count=0
txt_id = 1
for index,row in df.iterrows():
    #eviews=row['评论']
    reviews = row['text']
    review_split, review_pos, review_split_pos=fenci_and_pos(reviews)
    # print(review_split)
    # print(review_pos)
    # print(review_split_pos)
    # review_mysql_id=row['mysql_id']
    # print(review_mysql_id)  #输出当前分词的评论ID
    review_ouid=row['id']
    #print(review_ouid)

    df.loc[index,'review_split']=review_split
    df.loc[index,'review_pos']=review_pos
    df.loc[index,'review_split_pos']=review_split_pos
    #review_split 将分词结果逐行写入txt文档中if review_count<20000
    if review_count<10:
        review_count+=1  #计数+1
        review_split_txt_path = os.path.join(datapath,'split.txt')
        #review_split_txt_path = 'split_txt_' + str(txt_id) + '.txt'
        f = open(review_split_txt_path, 'a', encoding='utf-8')
        f.write('\n' + review_split)
        f.close()
    else:
        txt_id+=1
        review_count=0
        review_split_txt_path = os.path.join(datapath,'split.txt')
        #review_split_txt_path = 'split_txt_' + str(txt_id) + '.txt'
        f = open(review_split_txt_path, 'a', encoding='utf-8')
        f.write('\n' + review_split)
        f.close()

df.to_csv(os.path.join(datapath,'fenci.csv'), header=None, index=False)  # header=None指不把列号写入csv当中
# 计算分词与词性标注所用时间
end_time = time.time()
fenci_mins, fenci_secs = fenci_pos_time(start_time, end_time)
print(f'Fenci Time: {fenci_mins}m {fenci_secs}s')
print("done")
