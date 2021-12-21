# _*_ coding: utf-8 _*_
import os
import queue
from spider.CatalogSpider import CatalogSpider
from threads.SpiderThread import SpiderThread
# 导入配置参数
from config import THREAD_NUMBER
from config import SAVE_PATH
# 导入自定义数据结构
from items.ThreadItem import ThreadItem
# 导入合并最终爬虫内容功能
from tools.Merge import Merge
'''
URL: https://ssr1.scrape.center/
目标:   - 目录页的电影URL
        - 详细页
            - 电影标题
            - 电影类型
            - 电影评分
            - 电影海报（链接即可）
            - 上映地区
            - 上映时间
            - 电影时长
            - 剧情简介
            - 电影导演
要求: 多线程进行加速爬取，使用正则
'''

class Example(object):
    '''测试'''
    def __init__(self):
        self.api = "https://ssr1.scrape.center/"
        ThreadItem.queue_ = queue.Queue()
        

    def go(self) -> None:
        '''运行'''
        Example.exists_save_path()
        # 开始线程
        self.start_threads()
        # 队列添加任务
        self.put_tasks()
        # 等待队列完成
        ThreadItem.queue_.join()
        # 关闭线程
        self.stop_threads()
        # 合并
        Merge.to_json()


    def start_threads(self) -> None:
        '''开始线程'''
        if ThreadItem.threads is not None:
            raise AttributeError("线程列表不为空.")

        ThreadItem.threads = []
        for _ in range(THREAD_NUMBER):
            thread = SpiderThread()
            thread.start()
            ThreadItem.threads.append(thread)
    

    def stop_threads(self) -> None:
        '''关闭线程'''
        for thread in ThreadItem.threads:
            thread.stop()
        print("exit")


    def put_tasks(self) -> None:
        '''添加任务'''
        ThreadItem.queue_.put(CatalogSpider(self.api))


    @staticmethod
    def exists_save_path() -> None:
        '''创建存储目录'''
        if not os.path.exists(SAVE_PATH):
            os.mkdir(SAVE_PATH)


if __name__ == "__main__":
    Example().go()