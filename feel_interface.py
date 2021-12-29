#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/28
# @Author  : Jane
import os

import matplotlib.pyplot as plt
import numpy as np

from path import keyword,datapath,itempath

class Feeling:
    def __init__(self):
        self.label = ['积极', '消极']
        self.positive = []
        self.negative = []
        #with open('feeling/positive.txt', encoding='utf-8') as fr:
        with open(os.path.join(itempath,'dict','feeling\\positive.txt'), encoding='utf-8') as fr:
            for line in fr:
                self.positive.append(line.strip())

        with open(os.path.join(itempath,'dict','feeling\\negative.txt'), encoding='utf-8') as fr:
            for line in fr:
                self.negative.append(line.strip())
    #输入一个二维向量，多分类得到每个标签的概率
    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()
    #
    def getScore(self, content):
        pos = 0
        neg = 0
        label_pre = {}
        for p in self.positive:
            if p in content:
                pos+=1
        for n in self.negative:
            if n in content:
                neg+=1
        sm = self.softmax([pos, neg])
        for i, j in zip(self.label, list(sm)):
            label_pre[i] = j
        if pos == neg:
            return '中性'
        return self.label[np.argmax(self.softmax([pos, neg]))]

if __name__ == '__main__':
    fee = Feeling()
    info = {}
    from tqdm import tqdm
    fw = open(os.path.join(datapath,'results.txt'), 'w', encoding='utf-8')
    with open(os.path.join(datapath,'reviews.txt'), encoding='utf-8') as fr:
        fr.readline()
        for line in tqdm(fr):
            score = fee.getScore(line.strip())
            fw.write(line.strip()+'\t'+score+'\n')
            fw.flush()
            info[score] = info.setdefault(score, 0) + 1
    print(info)
    #plt饼状图，遍历字典info
    labels = []
    X = []
    for k, v in info.items():
        labels.append(k)
        X.append(v)

# 饼状图
# 中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
#font = FontProperties(fname='Songti.ttc')
#mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
#mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
#autopct ，show percet
#fracs = [10,10,10]
#fracs = [pos_count,neg_count]
explode = [0.1,0,0.1] # 0.1 凸出这部分，
#fig = plt.figure()
labels = '积极', '消极','中性'
plt.pie(X, labels=labels,explode=explode,autopct='%3.1f %%',
        shadow=True, labeldistance=1.1, startangle = 90,pctdistance = 0.6)
plt.title("EmotionPLTChart")
plt.savefig(os.path.join(datapath, 'emotions.jpg'), dpi = 360)
plt.show()
#
# plt.rcParams['font.sans-serif'] = ['SimHei']
#
# # labels=['积极','消极','中性']
# # X=[335,542,101]
# fig = plt.figure()
# plt.pie(X,labels=labels,autopct='%1.2f%%') #画饼图（数据，数据对应的标签，百分数保留两位小数点）
# plt.title("Pie chart")
# plt.show()
# #plt.savefig("PieChart.jpg")