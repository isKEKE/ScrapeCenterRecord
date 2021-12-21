# _*_ coding: utf-8 _*_
import requests
from fake_useragent import UserAgent
from ProxyIPSpider import USER_AGENT_PATH


class BaseSpider(object):
    '''爬虫基类'''
    def __init__(self, url: str):
        # 目标链接
        self.url = url
        self.response = None
        # 获得的数据
        self.datas = None
    

    def set_headers(self) -> dict:
        '''设置请求头'''
        return {
            "User-Agent": UserAgent(path=USER_AGENT_PATH).random
        }


    def send(self) -> None:
        '''发送请求, GET'''
        response = requests.get(self.url, headers=self.set_headers(),
                                timeout=(5, 10))
        response.encoding = "utf-8"
        self.response = response


    def parse(self) -> None:
        '''解析方法，需重构'''
        pass


    def go(self) -> None:
        '''运行'''
        try:
            self.send()
        except requests.exceptions.RequestException:
            # 异常信号，告诉线程需要把此对象重新放入队列
            raise AttributeError
        
        # 调用解析函数
        self.parse()