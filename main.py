import shutil
import runpy
import os

itempath = 'J:\Programming\Workplace\WeiboTopic\\'

if __name__ == '__main__':
    #1.获取路径
    runpy.run_path(os.path.join(itempath,'CreatePath.py'),run_name='__main__')
    runpy.run_path(os.path.join(itempath, 'path.py'), run_name='__main__')
    #2.爬虫
    runpy.run_path(os.path.join(itempath,'Spider.py'), run_name='__main__')
    #3.分词
    runpy.run_path(os.path.join(itempath,'cut_words.py'), run_name='__main__')
    #4.词频词云分析
    runpy.run_path(os.path.join(itempath, 'WordAnalyse.py'), run_name='__main__')
    #5.情感分析
    runpy.run_path(os.path.join(itempath, 'feel_interface.py'), run_name='__main__')