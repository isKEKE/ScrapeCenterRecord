# _*_ coding: utf-8 _*_
import re
import random
import os
import pickle
from items.MovieItem import MovieItem
from config import SAVE_PATH
from .BaseSpider import BaseSpider



class MovieSpider(BaseSpider):
    '''详细页爬虫'''
    patterns = [
            ('''<h2.*?="" class="m-b-sm">(.*?)</h2></a>''', "title"),
            ('''<button.*?el-button category el-button--primary el-button--mini.*?<span>(.*?)</span>''', "type_"),
            ('''score.*?(\d.\d)</p>''', "score"),
            ('''<p data.*? class="name text-center m-b-none m-t-xs">(.*?)</p></div>''', "director"),
            ('''<img.*?"([A-z]+://[^\s]*)"\s+class="cover">''', "poster"),
            ('''\d{4}-\d{2}-\d{2}''', "datetime_"),
            ('''剧情简介.*?<p.*?>[\s]+(.*?)\n''', "introd"),
            ('''/ </span>\n.*?<span data.*?>(.*?)</span>''', "time_"),
            ('''class="m-v-sm info".*?([\u4e00-\u9fa5、]+)</span>\n.*?/\s''', "area")
        ]
    def __init__(self, url: str):
        super(MovieSpider, self).__init__(url=url)
        # 存储对象
        self.movies = None


    def parse(self) -> None:
        '''解析'''
        # 源码
        html = self.response.text
        # 存储对象
        self.movies = MovieItem()
        # 超链接
        self.movies.url = self.response.url
        # 正则
        for pattern, key in self.patterns:
            value = ",".join(re.findall(pattern, html, re.S))
            setattr(self.movies, key, value)
        # 保存
        self.save_to_pc()


    def save_to_pc(self) -> None:
        '''保存'''
        title = self.movies.title or MovieSpider.random_name()
        name = "".join(re.findall("[0-9\u4e00-\u9fa5]+", title))
        # 路径
        filepath = os.path.join(SAVE_PATH, f"{name}.pkl")
        # 输出
        with open(filepath, "wb") as fp:
            pickle.dump(self.movies, fp)
        # 初始化
        self.movies = None
    
    
    @staticmethod
    def random_name() -> str:
        '''随机名字'''
        item_ = [str(n) for n in range(10)]
        random.shuffle(item_)
        return "".join(item_)