# /usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: yunrui
# __Date__:   2019/4/18

#从美食天下网上爬单个菜谱信息

import requests
import re
import mysql.connector

def getRecipeInfo(requestUrl):

    conn = mysql.connector.connect(user='root', password='123456', database='recipe')
    cursor = conn.cursor()

    headers = {
        "User-Agent": "Mozilla//5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }

    #输入菜谱单页
    url = requestUrl
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text

    id = re.findall(r'-(.*?)\.html', url)[0]

    title = re.findall(r'id="recipe_title" title="(.*?)">', html)
    if title:
        title = title[0]
    else:
        title = None

    author = re.findall(r'id="recipe_username">(.*?)<', html)
    if author:
        author = author[0]
    else:
        author = None

    J_photo = re.findall(r'<a class="J_photo".*?<img src="(.*?)" alt', html, re.S)
    if J_photo:
        J_photo = J_photo[0]
    else:
        J_photo = None

    abstract = re.findall(r'<div id="block_txt1"><span class="txt_tart">“</span>(.*?)<span class="txt_end">” </span>', html, re.S)
    if abstract:
        abstract = abstract[0]
        replace_list = [
            '<br>', '</br>', ' ', '<br />', '<br/>'
        ]
        for each in replace_list:
            abstract = abstract.replace(each, '')
    else:
        abstract = None

    raw_material_str = ''
    raw_material_info = re.findall(r'<legend>主料</legend>(.*?)</div>', html, re.S)
    if raw_material_info:
        raw_material_list = re.findall(r'<b>(.*?)</b>.*?"category_s2">(.*?)</span>', raw_material_info[0], re.S)
        if raw_material_list:
            for each in raw_material_list:
                raw_material_str = raw_material_str + each[0] + ',' + each[1] + ';'
        else:
            raw_material_str = None
    else:
        raw_material_str = None

    ingredients_str = ''
    ingredients_info = re.findall(r'<legend>辅料</legend>(.*?)</div>', html, re.S)
    if ingredients_info:
        ingredients_list = re.findall(r'<b>(.*?)</b>.*?"category_s2">(.*?)</span>', ingredients_info[0], re.S)
        if ingredients_list:
            for each in ingredients_list:
                ingredients_str = ingredients_str + each[0] + ',' + each[1] + ';'
        else:
            ingredients_str = None
    else:
        ingredients_str = None

    #口味、工艺、耗时、难度
    other_info = re.findall(r'<div class="recipeCategory_sub_R mt30 clear">(.*?)<div class="mo mt20">', html, re.S)
    if other_info:
        other_info = other_info[0]
        taste = re.findall(r'>(.*?)</a>\n</span>\n<span class="category_s2">口味</span>', other_info)
        if taste:
            taste = taste[0]
        else:
            taste = None

        technique = re.findall(r'>(.*?)</a>\n</span>\n<span class="category_s2">工艺</span>', other_info)
        if technique:
            technique = technique[0]
        else:
            technique = None
        
        time = re.findall(r'>(.*?)</a>\n</span>\n<span class="category_s2">耗时</span>', other_info)
        if time:
            time = time[0]
        else:
            time = None
        
        difficulty = re.findall(r'>(.*?)</a>\n</span>\n<span class="category_s2">难度</span>', other_info)
        if difficulty:
            difficulty = difficulty[0]
        else:
            difficulty = None

    #做法步骤
    step_str = ''
    step_list = re.findall(r'<img src="(.*?)" alt=".*?">\n</div>\n<div class="recipeStep_word"><div class="recipeStep_num">(.*?)</div>(.*?)</div>', html)
    if step_list:
        for each in step_list:
            step_str = step_str + each[1] + ':' + each[2] + '\n' + '图片链接：' + each[0]+'\n'
    else:
        step_str = None

    kitchen_utensils = re.findall(r'使用的厨具：(.*?)\n</div>', html)
    if kitchen_utensils:
        kitchen_utensils = kitchen_utensils[0]
    else:
        kitchen_utensils = None

    category_str = ''
    category_info = re.findall(r'所属分类：(.*?)<div class="recipeArction mt10 clear">', html, re.S)
    if category_info:
        category = re.findall(r'title="(.*?)"', category_info[0])
        if category:
            for each in category:
                category_str = category_str + ' ' + each
        else:
            category_str = None
    else:
        category_str = None

    tips = re.findall(r'<div class="recipeTip">(.*?)<div class="recipeTip mt16">\n来自 美食天下', html, re.S)
    if tips:
        tips = tips[0]
        replace_list = [
            '<br>', '</br>', ' ', '<br />', '<br/>', '</div>'
        ]
        for each in replace_list:
            tips = tips.replace(each, '')
    else:
        tips = None

    
    # 存入数据库
    cursor.execute('insert ignore into recipe_info (id, title, author, J_photo, abstract, raw_material_info, ingredients_info, taste, technique, time, difficulty, kitchen_utensils, category, tips, step) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [id, title, author, J_photo, abstract, raw_material_str, ingredients_str, taste, technique, time, difficulty, kitchen_utensils, category_str, tips, step_str])

    conn.commit()
    conn.close

    return

