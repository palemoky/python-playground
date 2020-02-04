# -*- coding: utf8 -*-

""""
学爬虫利器 XPath, 看这一篇就够了 https://zhuanlan.zhihu.com/p/29436838
 https://www.jianshu.com/p/cd3b80849613
 https://zhuanlan.zhihu.com/p/99810013
python lxml 教程 https://www.cnblogs.com/dahu-daqing/p/6749666.html
Python 最佳实践指南 https://pythonguidecn.readthedocs.io/zh/latest/

xlwt 针对 Ecxec2007 之前的版本，即.xls 文件，其要求单个 sheet 不超过 65535 行，而 openpyxl 则主要针对 Excel2007 之后的版本（.xlsx），它对文件大小没有限制。xlrd/xlwt的读写速度也优于openpyxl
"""

import xlwt
import requests
import lxml.etree

from time import sleep

header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

wb = xlwt.Workbook()
sheet = wb.add_sheet('Movie')
title = ('排名', '链接', '片名', '海报', '语录', '导演', '类型', '上映日期', '国家', '评分', '评价人数', 'IMDB 链接')
for index in range(len(title)):
    sheet.write(0, index, title[index])

"""
每页 25 条数据，共 10 页
"""
for start in range(0, 10):
    url = 'https://movie.douban.com/top250?start=' + str(start * 25) + '&filter='

    # 获取排行页内容并 XML 化处理
    list_page_selector = lxml.etree.HTML(requests.get(url, headers=header).text)

    for item in range(1, 26):
        base_xpath = '//*[@id="content"]/div/div[1]/ol/li[' + str(item)

        ranking = int(list_page_selector.xpath(base_xpath + ']/div/div[1]/em/text()')[0])
        link = list_page_selector.xpath(base_xpath + ']/div/div[2]/div[1]/a/@href')[0]
        movie_info = list_page_selector.xpath(base_xpath + ']/div/div[2]/div[2]/p[1]/text()[2]')[0].strip().split(' / ')

        # 获取影片详情页内容
        detail_page_selector = lxml.etree.HTML(requests.get(link, headers=header).text)

        movie = [
            ranking,  # Ranking
            link,  # Link
            detail_page_selector.xpath('//*[@id="content"]/h1/span[1]/text()')[0],  # Name
            list_page_selector.xpath(base_xpath + ']/div/div[1]/a/img/@src')[0].replace('s_ratio_poster', 'raw'),  # Poster
            list_page_selector.xpath(base_xpath + ']/div/div[2]/div[2]/p[2]/span/text()')[0],  # Quote
            detail_page_selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0],  # Director
            movie_info[2],  # Type
            # detail_page_selector.xpath('//*[@id="info"]/span[13]/text()'),  # Runtime  片长无法正常获取
            movie_info[0],  # Release Date
            movie_info[1],  # Country
            list_page_selector.xpath(base_xpath + ']/div/div[2]/div[2]/div/span[2]/text()')[0],  # Rating
            "{:,}".format(int(list_page_selector.xpath(base_xpath + ']/div/div[2]/div[2]/div/span[4]/text()')[0].replace('人评价', ''))),  # Ratings
            detail_page_selector.xpath('//*[@id="info"]/a/@href')[0]  # IMDB
        ]

        # 将数据填充入表格
        for index in range(len(movie)):
            sheet.write(ranking, index, movie[index])

    # 根据 https://movie.douban.com/robots.txt 得 Crawl-delay: 5
    sleep(5)

wb.save('./Douban_movie_top_250.xls')

print('DONE')
