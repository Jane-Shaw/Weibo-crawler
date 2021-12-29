#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Topic s1spider Without Cookie
Created 2021/09/22
author: Jane
"""

import os
import shutil
import random
import time
from urllib.parse import urlencode

import pandas as pd
import requests
from pyquery import PyQuery as pq

from path import keyword,datapath,itempath

#keyword = input("请输入需要爬取话题的名称：")

host = 'm.weibo.cn'
base_url = 'https://%s/api/container/getIndex?' % host
user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'

# 设置请求头
headers = {
    'Host': host,
    # 'Referer': 'https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E5%A6%82%E4%BD%95%E7%9C%8B%E5%BE%85%E5%8F%8D%E5%86%85%E5%8D%B7%E7%83%AD%E6%BD%AE%23&extparam=%23%E5%A6%82%E4%BD%95%E7%9C%8B%E5%BE%85%E5%8F%8D%E5%86%85%E5%8D%B7%E7%83%AD%E6%BD%AE%23&luicode=10000011&lfid=100103type%3D38%26q%3D%E5%86%85%E5%8D%B7%26t%3D0',
    'User-Agent': user_agent
}

# 按页数抓取数据
def get_single_page(page, keyword):
    #请求参数
    params = {
        #'containerid': f'{containerid}',  ##女子怀孕七个月被公司称没产假劝退 100103type=1&t=10&q=
        'containerid': f'100103type=1&t=10&q=#{keyword}#',  ##女子怀孕七个月被公司称没产假劝退 #231522type=1&t=10&q=
        'page_type': 'searchall',
        'page': page
    }

    url = base_url + urlencode(params)
    print(url)
    try:
        response = requests.get(url,headers = headers)
        #使用代理换ip
        # ,proxies=abstract_ip.get_proxy()
        if response.status_code == 200:
            return response.json()
    except:
        pass

#长文本爬取代码段
def getLongText(lid):
    #lid为长文本对应的id，长文本请求头
    headers_longtext = {
        'Host': host,
        'Referer': 'https://m.weibo.cn/status/' + lid,
        'User-Agent': user_agent
    }
    params = {
        'id': lid
    }
    url = 'https://m.weibo.cn/statuses/extend?' + urlencode(params)
    try:
        response = requests.get(url, headers=headers_longtext)
        # proxies=abstract_ip.get_proxy()
        if response.status_code == 200:
            #数据返回成功
            jsondata = response.json()
            tmp = jsondata.get('data')
            return pq(tmp.get("longTextContent")).text()
            #解析返回结构，获取长文本对应内容
    except:
        pass

# 解析页面返回的json数据
global count
count = 0

#修改后的页面爬取数据解析函数
#这大概是写入表格

def parase_page(json):
    global count
    items = json.get('data').get('cards')

    for item in items:
        try:
            topic = json.get('data').get('cardlistInfo').get('cardlist_head_cards')[0]
            topic = topic.get('head_data').get('title')
            item = item.get('mblog')
            if item:
                if item.get('isLongText') is False:
                    #不是长文本
                    data = {
                        #'topic': topic,
                        'id': item.get('id'),
                        'name': item.get('user').get('screen_name'),
                        #'user_id': item.get('user').get('id'),
                        #'sex': item.get('user').get('gender'),
                        'time': item.get('created_at'),
                        'text': pq(item.get("text")).text(),
                        # 仅提取内容中的文本
                        #'attitudes': item.get('attitudes_count'),
                        # 点赞数
                        #'comments': item.get('comments_count'),
                        # 评论数
                        #'reposts': item.get('reposts_count'),
                        # 转发数
                        #'text_Length': item.get('textLength'),
                    }
                else:
                    #长文本涉及文本展开部分
                    tmp = getLongText(item.get('id'))
                    #调用函数
                    data = {
                        #'topic': topic,
                        'id': item.get('id'),
                        'name': item.get('user').get('screen_name'),
                        #'user_id': item.get('user').get('id'),
                        #'sex': item.get('user').get('gender'),
                        'time': item.get('created_at'),
                        'text': tmp
                        # 仅提取内容中的文本
                        #'attitudes': item.get('attitudes_count'),
                        #'comments': item.get('comments_count'),
                        #'reposts': item.get('reposts_count'),
                        #'text_Length': item.get('textLength'),
                    }

                yield data
                count += 1

        except:
            import traceback
            print(traceback.format_exc())
            pass

#将爬取的csv转换为txt
def convert():

    filewrite = os.path.join(datapath,'reviews.txt')

    df=pd.read_csv(os.path.join(datapath, 'reviews.csv'),usecols=['text'],header=0,error_bad_lines=False,encoding='utf-8').astype(str)
    df.to_csv(filewrite,sep='\t',index=False)

    #正则处理数据删除掉关键词
    lineList = []
    #matchPattern = re.compile(r'#女子怀孕七个月被公司称没产假劝退#')
    file = open(filewrite,'r',encoding='utf-8')
    while 1:
        line = file.readline()
        if not line:
            print("Read File End or Error")
            break
        ##{keyword}#
        line2 = line.replace(f'#{keyword}#',' ')
        lineList.append(line2)

    file.close()
    #写入file
    file = open(filewrite,'w',encoding='UTF-8')
    for i in lineList:
        file.write(i)
    file.close()

    print("done")

    return 1

#keyword = '苹果多家供应商限电停产'
if __name__ == '__main__':
    keyword = keyword
    # keyword = '苹果多家供应商限电停产'
    # df = pd.DataFrame({col: [] for col in
    #                    ['topic', 'id', 'name', 'user_id', 'sex',
    #                     'created', 'text','attitudes', 'comments',
    #                     'reposts', 'text_Length']})
    df = pd.DataFrame({col: [] for col in
                       ['id', 'name','time', 'text']})
    #print(datapath)
    for page in range(1,5):
        # 瀑布流下拉式，加载200次（10次）
        print(page)
        json = get_single_page(page,keyword)
        for result in parase_page(json):
            #需要存入的字段
            df = df.append(result, ignore_index=True)

            if page % 3 == 0:
                #df.to_csv(f'{keyword}.csv', index=False, encoding='utf-8-sig')
                df.to_csv(os.path.join(datapath, 'reviews.csv'), index=False, encoding='utf-8-sig')

            time.sleep(random.randint(2, 6))
            #爬取时间间隔
    convert()

print("爬取并转换完毕！")






