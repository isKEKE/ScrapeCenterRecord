# _*_ coding: utf-8 _*_
import os
import glob
import pickle
import json
from config import SAVE_PATH


class Merge(object):
    '''合并爬虫内容为json存储'''
    @staticmethod
    def to_json() -> None:
        json_file = open(os.path.join(SAVE_PATH, f"movies.json"), "w")
        json_file.write("[")
        # 数量
        length = 0
        for filepath in glob.glob(f"{SAVE_PATH}/*.pkl"):
            length += 1
            with open(filepath, "rb") as fp:
                spider = pickle.load(fp)

            json_file.write(f"{json.dumps(spider.json())}, ")
            # 删除个体文件
            os.remove(filepath)
            
        json_file.write(f'{{"length":{length}}}]')
        json_file.close()


if __name__ == "__main__":
    Merge.to_json()