# _*_ coding: utf-8 _*_
import re
import urllib.parse
from items.ThreadItem import ThreadItem
from .BaseSpider import BaseSpider
from .MovieSpider import MovieSpider


class CatalogSpider(BaseSpider):
    '''目录爬虫'''
    api = "https://ssr1.scrape.center/"
    # RE表达式对象
    pattern_next = re.compile('''<a href="(.*?)" class="next">''')
    pattern_movie = re.compile('''<a .*?="" href="(.*?)" class="name">''')
    def __init__(self, url: str):
        super(CatalogSpider, self).__init__(url=url)
        
    
    def parse(self) -> None:
        '''解析'''
        # 通过爬虫过程打印信息看到速度不是特别理想，这里是因为正则原因。
        element_next = re.findall(self.pattern_next, self.response.text)
        if element_next:
            # 翻页
            next_url = urllib.parse.urljoin(self.api, "".join(element_next))
            # 添加到队列
            ThreadItem.queue_.put(CatalogSpider(next_url))

        # 详细页
        elements_href = re.findall(self.pattern_movie, self.response.text)
        for href in elements_href:
            movie_url = urllib.parse.urljoin(self.api, href)
            movie_spider = MovieSpider(movie_url)
            # 详细界面爬虫对象放入线程队列
            ThreadItem.queue_.put(movie_spider)
