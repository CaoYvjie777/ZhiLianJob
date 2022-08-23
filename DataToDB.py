# 将csv文件导入mongodb数据库

import pandas as pd
from pymongo import MongoClient

# mongodb://localhost/ 数据库连接地址
client = MongoClient("mongodb://localhost/")
# user 数据库名称
db = client["ZhiLianJob"]
# table 集合名称
citys = {'上海': 538, '北京': 530, '广州': 763, '深圳': 765, '天津': 531, '武汉': 736, '西安': 854, '成都': 801, '南京': 635, '杭州': 653,
         '重庆': 551, '厦门': 682}
for i in citys.keys():
    file_name = 'E:/classes/Python/爬虫作业/智联招聘数据/' + i + '.csv'
    product_summary = db[i]
    # table_name csv数据内容
    data = pd.read_csv(file_name)
    for index, row in data.T.to_dict().items():
        product_summary.insert_one(row)
