# _*_ coding: utf-8 _*_

class ThreadItem(object):
    '''此类专门记录线程的数据结构'''
    # 线程列表
    threads: list = None
    
    # 队列对象
    queue_: 'queue.Queue' = None