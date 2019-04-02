# /usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: yunrui
# __Date__:   2019/3/27

#从美食天下网上爬全部菜谱列表

import requests
import re

def getRecipeList():
    headers = {
        "User-Agent": "Mozilla//5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }
    fb = open('全部菜谱链接列表.txt', 'w', encoding='utf-8')
    page_num = 1
    has_next_page = True
    all_list = []

    while has_next_page:
        next_page_link = 'https://home.meishichina.com/recipe-list-page-%d.html' % page_num
        response = requests.get(url=next_page_link, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        recipe_link_info = re.findall(r'<div class="ui_newlist_1 get_num" id="J_list">(.*?)<script', html, re.S)[0]
        recipe_link_list = re.findall(r'<div class="pic">\n<a target="_blank" href="(.*?)" title="(.*?)">', recipe_link_info)
        
        for each in recipe_link_list:
            all_list.append(each)
            fb.write(each[0])
            fb.write(' ')
            fb.write(each[1])
            fb.write('\n')
        page_num = page_num + 1
        has_next_page = re.findall(r'下一页', html)
    return all_list