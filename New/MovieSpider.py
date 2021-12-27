# _*_ coding: utf-8 _*_
import random
import os
import pickle
import re
import parsel
from items.MovieItem import MovieItem
from config import SAVE_PATH
from .BaseSpider import BaseSpider



class MovieSpider(BaseSpider):
    '''详细页爬虫'''
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
        # parsel解析
        selector = parsel.Selector(text=html)
        contents = selector.xpath('''//div[contains(@class, "p-h")]''')
        # 标题
        self.movies.title = contents.xpath(".//h2/text()").get()
        # 类型
        self.movies.type_ = contents.xpath('''./div[contains(@class, "categories")]//span/text()''').getall()
        # 二次筛选
        spans = contents.xpath('''./div[contains(@class, "m-v-sm")]/span/text()''')
        # 上映时间
        self.movies.datetime_ = spans.re("\d{4}-\d{2}-\d{2}")
        # 电影时间
        self.movies.time_ = spans.re("(\d+).*分钟")
        # 地区
        self.movies.area = spans.re("[^\d\s\u5206\u949f\u4e0a\u6620/-]+")
        # 简介
        self.movies.introd = contents.xpath('''//div[contains(@class, "drama")]//text()''').re("[^\s]+")
        # 分数
        self.movies.score = selector.xpath('''//p[contains(@class, "score")]/text()''').re("\d.\d")
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