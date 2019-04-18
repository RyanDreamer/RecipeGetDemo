# /usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: yunrui
# __Date__:   2019/4/2
# Last_modified_time: 2019/4/4

#从美食天下网上爬全部菜谱列表

import requests
import re
from ShowProcess import ShowProcess

import mysql.connector

def getRecipeList():
    headers = {
        "User-Agent": "Mozilla//5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }

    page_num = 1
    has_next_page = True
    all_list = []

    conn = mysql.connector.connect(user='root', password='123456', database='recipe')
    cursor = conn.cursor()

    max_steps = 1000    #有1k页数据
    process_bar = ShowProcess(max_steps)

    print('正在收集菜谱(预估时间20分钟)，已完成：\n')

    while has_next_page:
        process_bar.showProcess(page_num-1)

        next_page_link = 'https://home.meishichina.com/recipe-list-page-%d.html' % page_num
        response = requests.get(url=next_page_link, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        recipe_link_info = re.findall(r'<div class="ui_newlist_1 get_num" id="J_list">(.*?)<script', html, re.S)[0]
        recipe_link_list = re.findall(r'<div class="pic">\n<a target="_blank" href="(.*?)" title="(.*?)">', recipe_link_info)

        new_list = []
        for each in recipe_link_list:
            recipe_id = re.findall(r'-(.*?)\.html', each[0])[0]
            new_list.append([recipe_id, each[0], each[1]])
        recipe_link_list = new_list

        for each in recipe_link_list:
            all_list.append(each)
            cursor.execute('SET NAMES utf8mb4')
            cursor.execute('insert ignore into recipe_list (id, title, url) values (%s, %s, %s)', [each[0], each[2], each[1]])
            conn.commit()

        page_num = page_num + 1
        has_next_page = re.findall(r'下一页', html)
    
    process_bar.showProcess(page_num-1)

    conn.commit()
    cursor.close()

    return all_list