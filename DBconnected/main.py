# /usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: yunrui
# __Date__:   2019/3/31
# Last_modified_time: 2019/4/4


from recipeInfo import getRecipeInfo
from recipeList import getRecipeList
from ShowProcess import ShowProcess

r_list = getRecipeList()
max_steps = 10000
process_bar = ShowProcess(max_steps)
print('正在获取菜谱单页并生成文件...已完成：\n')

for index in list(range(r_list)):
    process_bar.showProcess(index)
    getRecipeInfo(r_list[index][0])

process_bar.showProcess(index)