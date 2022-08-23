
import requests
import re
from copyheaders import headers_raw_to_dict
from bs4 import BeautifulSoup
import pandas as pd

# 根据url和参数获取网页的HTML：

def get_html(url, params):

    req = requests.get(url,params=params)
    req.encoding = req.apparent_encoding
    html = req.text

    return html


# 输入url和城市编号，获取由所有职位信息的html标签的字符串组成的列表：

def get_html_list(url, city_num):

    html_list = list()

    for i in range(1, 2):
        params = {'jl': str(city_num), 'kw': '数据分析师', 'p': str(i)}
        html = get_html(url, params)
        soup = BeautifulSoup(html, 'html.parser')
        html_list += soup.find_all(name='a', attrs={'class': 'joblist-box__iteminfo iteminfo'})

    for i in range(len(html_list)):
        html_list[i] = str(html_list[i])

    return html_list


# 根据上面的HTML标签列表，把每个职位信息的有效数据提取出来，保存csv文件：

def get_csv(html_list):

    # city = position = company_name = company_size = company_type = salary = education = ability = experience = evaluation = list()  #
    # 上面赋值方法在这里是错误的，它会让每个变量指向同一内存地址，如果改变其中一个变量，其他变量会同时发生改变

    # table = pd.DataFrame(columns = ['城市','职位名称','公司名称','公司规模','公司类型','薪资','学历要求','技能要求','工作经验要求'])
    city, position, company_name, company_size, company_type, salary, education, ability, experience = ([] for i in range(9))  # 多变量一次赋值

    for i in html_list:

        if re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i):
            s = re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i).group(1)
            city.append(s)
            s = re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i).group(2)
            experience.append(s)
            s = re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i).group(3)
            education.append(s)
        else:
            city.append(' ')
            experience.append(' ')
            education.append(' ')


        if re.search('<span class="iteminfo__line1__jobname__name" title="(.*?)">', i):
            s = re.search('<span class="iteminfo__line1__jobname__name" title="(.*?)">', i).group(1)
            position.append(s)
        else:
            position.append(' ')

        if re.search('<span class="iteminfo__line1__compname__name" title="(.*?)">', i):
            s = re.search('<span class="iteminfo__line1__compname__name" title="(.*?)">', i).group(1)
            company_name.append(s)
        else:
            company_name.append(' ')

        if re.search(
                '<span class="iteminfo__line2__compdesc__item">(.*?) </span> <span class="iteminfo__line2__compdesc__item">(.*?) </span>',
                i):
            s = re.search(
                '<span class="iteminfo__line2__compdesc__item">(.*?) </span> <span class="iteminfo__line2__compdesc__item">(.*?) </span>',
                i).group(1)
            company_type.append(s)
            s = re.search(
                '<span class="iteminfo__line2__compdesc__item">(.*?) </span> <span class="iteminfo__line2__compdesc__item">(.*?) </span>',
                i).group(2)
            company_size.append(s)
        else:
            company_type.append(' ')
            company_size.append(' ')

        if re.search('<p class="iteminfo__line2__jobdesc__salary">([\s\S]*?)<', i):
            s = re.search('<p class="iteminfo__line2__jobdesc__salary">([\s\S]*?)<', i).group(1)
            s = s.strip()
            salary.append(s)
        else:
            salary.append(' ')

        s = str()
        l = re.findall('<div class="iteminfo__line3__welfare__item">.*?</div>', i)
        for i in l:
            s = s + re.search('<div class="iteminfo__line3__welfare__item">(.*?)</div>', i).group(1) + ' '
        ability.append(s)

    table = list(zip(city, position, company_name, company_size, company_type, salary, education, ability, experience))

    return table



if __name__ == '__main__':

    url = 'https://sou.zhaopin.com/'
    citys = {'上海':538, '北京':530, '广州':763, '深圳':765, '天津':531, '武汉':736, '西安':854, '成都':801, '南京':635, '杭州':653, '重庆':551, '厦门':682}
    for i in citys.keys():
        html_list = get_html_list(url, citys[i])
        table = get_csv(html_list)
        df = pd.DataFrame(table, columns=['city', 'position', 'company_name', 'company_size', 'company_type', 'salary',
                                          'education', 'ability', 'experience'])
        file_name = 'E:/classes/Python/爬虫作业/智联招聘数据/'+i + '.csv'
        df.to_csv(file_name)




