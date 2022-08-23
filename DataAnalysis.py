
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# coding: UTF-8
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号#有中文出现的情况，需要u'内容'

import re
import os
import seaborn as sns
from wordcloud import WordCloud

citys = ['上海', '北京', '广州', '深圳', '天津', '武汉', '西安', '成都', '南京', '杭州', '重庆', '厦门']


# 数据清洗：

def data_clear():
    for i in citys:

        file_name = 'E:/classes/Python/爬虫作业/智联招聘数据/' + i + '.csv'
        df = pd.read_csv(file_name, index_col=0)

        for i in range(0, df.shape[0]):

            s = df.loc[[i], ['salary']].values.tolist()[0][0]
            if re.search('(.*)-(.*)', s):
                a = re.search('(.*)-(.*)', s).group(1)
                if a[-1] == '千':
                    a = eval(a[0:-1]) * 1000
                elif a[-1] == '万':
                    a = eval(a[0:-1]) * 10000
                b = re.search('(.*)-(.*)', s).group(2)
                if b[-1] == '千':
                    b = eval(b[0:-1]) * 1000
                elif b[-1] == '万':
                    b = eval(b[0:-1]) * 10000
                s = (a + b) / 2
                df.loc[[i], ['salary']] = s
            else:
                df.loc[[i], ['salary']] = ''

        os.remove(file_name)
        df.to_csv(file_name)


# 各个城市数据分析职位数量条形图:

def citys_jobs():
    job_num = list()
    for i in citys:
        file_name = 'E:/classes/Python/爬虫作业/智联招聘数据/' + i + '.csv'
        df = pd.read_csv(file_name, index_col=0)
        job_num.append(df.shape[0])
    df = pd.DataFrame(list(zip(citys, job_num)))
    df = df.sort_values(1, ascending=False)
    x = list(df[0])
    y = list(df[1])

    fig = plt.figure(dpi=200)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.bar(x, y, alpha=0.8)
    ax.set_title('数据分析职位在全国主要城市的数量分布')
    ax.set_ylim(0, 350)

    plt.savefig('E:/classes/Python/爬虫作业/DataAnalysisResult/数据分析职位在全国主要城市的数量分布.jpg')
    plt.show()


# 不同城市薪资分布条形图：

def citys_salary():
    y = list()
    x = citys

    for i in citys:
        file_name = 'E:/classes/Python/爬虫作业/智联招聘数据/' + i + '.csv'
        df = pd.read_csv(file_name, index_col=0)
        y0 = df['salary'].mean()
        y.append(round(y0 / 1000, 1))

    df = pd.DataFrame(list(zip(x, y)))
    df = df.sort_values(1, ascending=False)
    x = list(df[0])
    y = list(df[1])

    fig = plt.figure(dpi=200)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.bar(x, y, alpha=0.8)
    ax.set_title('数据分析职位在一些主要城市的薪资分布（单位：千）')
    ax.set_ylim(5, 18)
    for a, b, label in zip(x, y, y):  # 内置函数zip()：将几个列表合并为二维列表并转置，返回一个特殊对象，可通过list()列表化之后查看
        plt.text(a, b, label, horizontalalignment='center', fontsize=10)  # plt.text()函数：在图中（a,b)位置添加一个文字标签label

    plt.savefig('E:/classes/Python/爬虫作业/DataAnalysisResult/数据分析职位在一些主要城市的薪资分布.jpg')
    plt.show()


# 数据分析岗位总体薪资的分布

def salary_distribute():
    salary_list = list()
    for i in citys:
        file_name = 'E:/classes/Python/爬虫作业/智联招聘数据/' + i + '.csv'
        df = pd.read_csv(file_name, index_col=0)
        salary_list += list(df['salary'])
    salarys = list()
    for i in range(len(salary_list)):
        if not pd.isnull(salary_list[i]):  # 由于该列表是从pandas中读出的数据，故不能用if salary_list[i] == np.nan，会识别不出来
            salarys.append(round(salary_list[i] / 1000, 1))
    mean = np.mean(salarys)

    plt.figure(dpi=200)
    sns.distplot(salarys, hist=True, kde=True, kde_kws={"color": "r", "lw": 1.5, 'linestyle': '-'})
    plt.axvline(mean, color='r', linestyle=":")
    plt.text(mean, 0.01, '平均薪资: %.1f千' % (mean), color='r', horizontalalignment='center', fontsize=15)
    plt.xlim(0, 50)
    plt.xlabel('薪资分布（单位：千）')
    plt.title('数据分析职位整体薪资分布')
    plt.savefig('E:/classes/Python/爬虫作业/DataAnalysisResult/数据分析职位整体薪资分布.jpg')
    plt.show()


# 数据分析职位对学历要求的分布

def education_distribute():
    table = pd.DataFrame()
    for i in citys:
        file_name = 'E:/classes/Python/爬虫作业/智联招聘数据/' + i + '.csv'
        df = pd.read_csv(file_name, index_col=0)
        table = pd.concat([table, df])
    table = pd.DataFrame(pd.value_counts(table['education']))
    table = table.sort_values(['education'], ascending=False)
    x = list(table.index)
    y = list(table['education'])
    print(x)

    fig = plt.figure(dpi=200)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    explode = (0, 0, 0, 0.2, 0.4, 0.6, 0.8)
    ax.axis('equal')
    ax.pie(y, labels=x, autopct='%.1f%%', explode=explode)  # auto爬虫作业t显示每块饼的百分比属性且自定义格式化字符串，其中%%表示字符串%，类似正则
    ax.set_title('数据分析职位对学历要求的占比')
    ax.legend(x, loc=1)
    plt.savefig(r'E:/classes/Python/爬虫作业/DataAnalysisResult/数据分析职位对学历要求的占比.jpg')
    plt.show()


# 技能关键词频统计

def wordfrequence():
    table = pd.DataFrame()
    for i in citys:
        file_name = 'E:/classes/Python/爬虫作业/智联招聘数据/' + i + '.csv'
        df = pd.read_csv(file_name, index_col=0)
        table = pd.concat([table, df])
    l1 = list(table['ability'])
    l2 = list()
    for i in range(len(l1)):
        if not pd.isnull(l1[i]):
            l2.append(l1[i])
    words = ''.join(l2)

    cloud = WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体文件获取路径，默认字体不支持中文
        background_color='white',  # 设置背景颜色  默认是black
        max_words=20,  # 词云显示的最大词语数量
        random_state=1,  # 设置随机生成状态，即多少种配色方案
        collocations=False,  # 是否包括词语之间的搭配，默认True，可能会产生语意重复的词语
        width=1200, height=900  # 设置大小，默认图片比较小，模糊
    ).generate(words)
    plt.figure(dpi=200)
    plt.imshow(cloud)  # 该方法用来在figure对象上绘制传入图像数据参数的图像
    plt.axis('off')  # 设置词云图中无坐标轴
    plt.savefig("E:/classes/Python/爬虫作业/DataAnalysisResult/技能关键词频统计.jpg")
    plt.show()


if __name__ == "__main__":
    print("=====================# 数据清洗 #====================")
    data_clear()
    print("=====================# 各个城市数据分析职位数量条形图 #====================")
    citys_jobs()
    print("=====================# 不同城市薪资分布条形图 #====================")
    citys_salary()
    print("=====================# 数据分析岗位总体薪资的分布 #====================")
    salary_distribute()
    print("=====================# 数据分析职位对学历要求的分布 #====================")
    education_distribute()
    print("=====================# 技能关键词频统计 #====================")
    wordfrequence()

