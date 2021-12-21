# _*_ coding: utf-8 _*_
import threading
import queue
from items.ThreadItem import ThreadItem


class SpiderThread(threading.Thread):
    '''爬虫线程'''
    # 线程共享队列对象
    def __init__(self):
        super(SpiderThread, self).__init__()
        # 线程状态
        self.flag = True
        # 爬虫对象
        self.spider: 'BaseSpider' = None


    def run(self) -> None:
        '''运行'''
        while True:
            if self.flag == False:
                break
            try:
                # 阻塞模式
                self.spider = ThreadItem.queue_.get()
            except queue.Empty:
                pass
            else:
                if self.spider == -1:
                    continue

                # 执行
                self.execute()

                # 通知队列此次完成
                ThreadItem.queue_.task_done()


    def stop(self) -> None:
        '''线程停止'''
        self.flag = False
        ThreadItem.queue_.put(-1)
    

    def execute(self) -> None:
        '''执行爬虫对象方法'''
        try:
            self.spider.go()
        except AttributeError:
            # 异常, 对象重新放入队列
            ThreadItem.queue_.put(self.spider)
        else:
            print("线程任务 =>",self.ident, self.spider.response.url, 
                  ThreadItem.queue_.qsize())
