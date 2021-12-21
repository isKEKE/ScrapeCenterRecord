# _*_ coding: utf-8 _*_

'''
- 电影标题
- 电影类型
- 电影评分
- 电影海报（链接即可）
- 上映地区
- 上映时间
- 电影时长
- 剧情简介
- 电影导演
'''

class MovieItem(object):
    '''专门存储信息的数据结构'''
    __attrs__ = ["url", "title", "type_", "score", "time_", "director", 
                 "poster", "area", "datetime_", "introd"]
    def __init__(self):
        # 电影链接
        self.url = None
        # 电影标题
        self.title = None
        # 电影类型
        self.type_ = None
        # 电影评分
        self.score = None
        # 电影时长
        self.time_ = None
        # 电影导演
        self.director = None
        # 海报链接
        self.poster = None
        # 上映地区
        self.area = None
        # 上映时间
        self.datetime_ = None
        # 剧情简介
        self.introd = None
    

    def json(self) -> dict:
        '''整合为dict'''
        datas = {}
        for attr_name in MovieItem.__attrs__:
            value = getattr(self, attr_name)
            datas[attr_name] = value
        
        return datas


if __name__ == "__main__":
    item = MovieItem()
    item.title = "夏洛特烦恼"
    print(item.json())
