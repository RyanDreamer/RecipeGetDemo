# /usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: yunrui
# __Date__:   2019/3/27

#从美食天下网上爬单个菜谱信息

import requests
import re

def getRecipeInfo(requestUrl):

    headers = {
        "User-Agent": "Mozilla//5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }

    #输入菜谱单页
    url = requestUrl
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    title = re.findall(r'id="recipe_title" title="(.*?)">', html)
    if title:
        title = title[0]
        fb = open('%s.txt' % title, 'w', encoding='utf-8')
    else:
        exit
    

    fb.write('菜名：')
    fb.write(title)
    fb.write('\n')

    fb.write('作者：')
    author = re.findall(r'id="recipe_username">(.*?)<', html)
    if author:
        author = author[0]
        fb.write(author)
    fb.write('\n')

    fb.write('预览图片：')
    J_photo = re.findall(r'<a class="J_photo".*?<img src="(.*?)" alt', html, re.S)
    if J_photo:
        fb.write(J_photo[0])
    else:
        fb.write('无')
    fb.write('\n')

    fb.write('简介：')
    abstract = re.findall(r'<div id="block_txt1"><span class="txt_tart">“</span>(.*?)<span class="txt_end">” </span>', html, re.S)
    if abstract:
        abstract = abstract[0]
        replace_list = [
            '<br>', '</br>', ' ', '<br />', '<br/>'
        ]
        for each in replace_list:
            abstract = abstract.replace(each, '')
        abstract = abstract.replace('\n', '\n\t')
        fb.write('\n\t')
        fb.write(abstract)
    else:
        fb.write('无')
    fb.write('\n')

    fb.write('食材明细：\n')
    fb.write('\t1)主料：')
    raw_material_info = re.findall(r'<legend>主料</legend>(.*?)</div>', html, re.S)
    if raw_material_info:
        raw_material_list = re.findall(r'<b>(.*?)</b>.*?"category_s2">(.*?)</span>', raw_material_info[0], re.S)
        if raw_material_list:
            for each in raw_material_list:
                fb.write(each[0])
                fb.write(',')
                fb.write(each[1])
                fb.write(';')
        else:
            fb.write('暂不明确')
    else:
        fb.write('暂不明确')
    fb.write('\n')

    fb.write('\t2)辅料：')
    ingredients_info = re.findall(r'<legend>辅料</legend>(.*?)</div>', html, re.S)
    if ingredients_info:
        ingredients_list = re.findall(r'<b>(.*?)</b>.*?"category_s2">(.*?)</span>', ingredients_info[0], re.S)
        if ingredients_list:
            for each in ingredients_list:
                fb.write(each[0])
                fb.write(',')
                fb.write(each[1])
                fb.write(';')
        else:
            fb.write('暂不明确')
    else:
        fb.write('暂不明确')
    fb.write('\n')

    recipe_material = (raw_material_list, ingredients_list)

    #口味、工艺、耗时、难度
    other_info = re.findall(r'<div class="recipeCategory_sub_R mt30 clear">(.*?)<div class="mo mt20">', html, re.S)
    if other_info:
        other_info = other_info[0]
        fb.write('口味：')
        taste = re.findall(r'>(.*?)</a>\n</span>\n<span class="category_s2">口味</span>', other_info)
        if taste:
            taste = taste[0]
            fb.write(taste)
        else:
            fb.write('暂不明确')
        fb.write('\n')

        fb.write('工艺：')
        technique = re.findall(r'>(.*?)</a>\n</span>\n<span class="category_s2">工艺</span>', other_info)
        if technique:
            technique = technique[0]
            fb.write(technique)
        else:
            fb.write('暂不明确')
        fb.write('\n')
        
        fb.write('耗时：')
        time = re.findall(r'>(.*?)</a>\n</span>\n<span class="category_s2">耗时</span>', other_info)
        if time:
            time = time[0]
            fb.write(time)
        else:
            fb.write('暂不明确')
        fb.write('\n')
        
        fb.write('难度：')
        difficulty = re.findall(r'>(.*?)</a>\n</span>\n<span class="category_s2">难度</span>', other_info)
        if difficulty:
            difficulty = difficulty[0]
            fb.write(difficulty)
        else:
            fb.write('暂不明确')
        fb.write('\n')


    #做法步骤
    fb.write('做法步骤：\n')
    step_list = re.findall(r'<img src="(.*?)" alt=".*?">\n</div>\n<div class="recipeStep_word"><div class="recipeStep_num">(.*?)</div>(.*?)</div>', html)
    if step_list:
        for each in step_list:
            fb.write('\t')
            fb.write(each[1])
            fb.write('：')
            fb.write(each[2])
            fb.write('\n\t')
            fb.write('图片链接：')
            fb.write(each[0])
            fb.write('\n')
    else:
        fb.write('暂不明确\n')

    fb.write('使用的厨具：')
    kitchen_utensils = re.findall(r'使用的厨具：(.*?)\n</div>', html)
    if kitchen_utensils:
        kitchen_utensils = kitchen_utensils[0]
        fb.write(kitchen_utensils)
    else:
        fb.write('暂不明确')
    fb.write('\n')

    fb.write('所属分类：')
    category_info = re.findall(r'所属分类：(.*?)<div class="recipeArction mt10 clear">', html, re.S)
    if category_info:
        category = re.findall(r'title="(.*?)"', category_info[0])
        if category:
            for each in category:
                fb.write(' ')
                fb.write(each)
        else:
            fb.write('暂不明确')
    else:
        fb.write('暂不明确')
    fb.write('\n')

    fb.write('小窍门：')
    tips = re.findall(r'<div class="recipeTip">(.*?)<div class="recipeTip mt16">\n来自 美食天下', html, re.S)
    if tips:
        tips = tips[0]
        replace_list = [
            '<br>', '</br>', ' ', '<br />', '<br/>', '</div>'
        ]
        for each in replace_list:
            tips = tips.replace(each, '')
        fb.write(tips)
    else:
        fb.write('暂不明确\n')

    return

