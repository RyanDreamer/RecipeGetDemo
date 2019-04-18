# /usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: yunrui
# __Date__:   2019/3/31
# Last_modified_time: 2019/4/4


from recipeInfo import getRecipeInfo
from recipeList import getRecipeList
from ShowProcess import ShowProcess

import mysql.connector

conn = mysql.connector.connect(user='root', password='123456', database='recipe')
cursor = conn.cursor()

cursor.execute('select * from recipe_list')
r_list = cursor.fetchall()
# if len(r_list) < 10000:
#     r_list = getRecipeList()

max_steps = r_list.__len__()
process_bar = ShowProcess(max_steps)
print('已得到%d条记录。' % max_steps)
print('正在获取菜谱单页...已完成：\n')

for index in list(range(max_steps)):
    process_bar.showProcess(index)
    getRecipeInfo(r_list[index][2])

process_bar.showProcess(index)