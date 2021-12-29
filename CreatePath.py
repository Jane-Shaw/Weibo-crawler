import os
import shutil

# print('\n')
#from s1spider.WithoutCookie import keyword

# 创造话题文件夹——如果有就删除再创造
#datapath = os.path.join(openFile(defaultpath, keyword), 'reviews.csv')
#print(datapath)
keyword = input("请输入需要爬取话题的名称：")

if __name__ == '__main__':
    itempath = 'J:\Programming\Workplace\WeiboTopic\\'
    defaultpath = 'J:\Programming\Workplace\WeiboTopic\WeiboData\\'


    def openFile(path, fileName):
        open = path + fileName
        # print(open)
        if os.path.exists(open):
            shutil.rmtree(open)
            # os.remove(open)
            #input('w')
        os.makedirs(open)
        return open

    datapath = openFile(defaultpath, keyword)
# print(keyword)
# print(datapath)

    lineList = [itempath,defaultpath,datapath,keyword]
    with open('path.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(lineList))
