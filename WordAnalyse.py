import os
import numpy as np
import wordcloud
from PIL import Image
# import pylab as mpl  # import matplotlib as mpl
from wordcloud import ImageColorGenerator
import jieba.analyse
import pandas as pd
import jieba.analyse
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from path import keyword,datapath,itempath


fontpath = os.path.join(itempath,'dict','Songti.ttc')

def cloud():
    font = FontProperties(fname=fontpath)
    #plt.rcParams['font.sans-serif'] = ['SimHei']

    #mk = imageio.imread("background.png")
    image = Image.open(os.path.join(itempath,'dict', 'background.png'))
    graph = np.array(image)

    # 构建并配置词云对象w
    w = wordcloud.WordCloud(
                            max_words=50,  # 词云显示的最大词数
                            background_color='white',
                            #mask=mk,
                            mask=graph,
                            font_path=fontpath, #字体路径，文件中没有(应该是无效设置)
                            )

    #设置分词结果保存的txt路径
    txt_id = 1
    review_split_txt_path = os.path.join(datapath,'split.txt')
    f = open(review_split_txt_path, 'r', encoding='utf-8')
    string=""
    for line in f.readlines():
        string+=line
    print(string)

    image_color = ImageColorGenerator(graph)


    # 将string变量传入w的generate()方法，给词云输入文字
    w.generate(string)
    # 将词云图片导出到当前文件夹
    w.to_file(os.path.join(datapath, 'cloud.png'))

def key():
    txt_id = 1
    split_path = os.path.join(datapath, 'split.txt')
    f = open(split_path, 'r', encoding='utf-8')
    review_split = " "
    for line in f.readlines():
        review_split += line
    # print("review_split:"+review_split)

    # test_reviews="刚刚才离开酒店，这是一次非常愉快满意住宿体验。"
    # review_split, review_pos, review_split_pos=fenci_and_pos(test_reviews)
    # print(review_split)
    # k = jieba.analyse.extract_tags(review_split,topK = 10)
    # print(k)

    keywords = jieba.analyse.extract_tags(review_split, topK=10, withWeight=True)
    print('【TF-IDF提取的关键词列表：】')
    print(keywords)  # 采用默认idf文件提取的关键词

    # 写入txt
    df = pd.DataFrame(keywords)
    # print(df)
    df.to_csv(os.path.join(datapath, 'data_keywords.txt'), index=None, header=None)


def keybarchart():
    font = FontProperties(fname=fontpath)
    bar_width = 0.5
    lyric = ''
    lyric_path = os.path.join(datapath, 'split.txt')
    f = open(lyric_path, 'r', encoding='utf-8')
    # review_split=''
    for i in f:
        lyric += f.read()
    # 前10的关键词
    result = jieba.analyse.textrank(lyric, topK=10, withWeight=True)
    # print(result)   #采用默认idf文件提取的关键词
    keywords1= dict()
    print(keywords1)

    for i in result:
        keywords1[i[0]] = i[1]
    print('关键词导入完毕\n')

    x = []
    y = []
    for key in keywords1:
        x.append(key)
    y.append(keywords1[key])
    num = len(x)
    fig = plt.figure(figsize=(28, 10))
    plt.bar(range(num), y, tick_label=x, width=bar_width)
    # 横坐标10
    plt.xticks(rotation=50, fontproperties=font, fontsize=10)
    plt.yticks(fontsize=20)
    plt.title("words-frequency chart", fontproperties=font, fontsize=30)
    plt.savefig(os.path.join(datapath, 'barchart.jpg'), dpi=360)
    plt.show()

#词频统计函数
def wordfreqcount():
    split_path = os.path.join(datapath, 'split.txt')
    wordfreq = {}  # 词频字典
    f = open(split_path, 'r', encoding='utf-8') #打开分词结果的txt文件
    review_split = ""
    #逐行读取文件，将读取的字符串用/切分，遍历切分结果，统计词频
    for line in f.readlines():
        review_words = line.split(" ")
        #print(review_words)
        keys = list(wordfreq.keys())
        for word in review_words:
            if word == '\n' or word == '' or word == ' ':
                continue
            if word in keys:
                wordfreq[word] = wordfreq[word] + 1
            else:
                wordfreq[word] = 1

    word_freq_list = list(wordfreq.items())
    word_freq_list.sort(key=lambda x: x[1], reverse=True)

    # 输出词频前10的词汇及其出现频次
    for i in range(50):
        print(word_freq_list[i])

    df = pd.DataFrame(word_freq_list)
    df.to_csv(os.path.join(datapath, 'wordfrequence.csv'), index=None, header=None)

    return word_freq_list

if __name__ == '__main__':
    key()
    cloud()
    word_freq_list = wordfreqcount()
    #keybarchart()
