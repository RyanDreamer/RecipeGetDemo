# /usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: yunrui
# __Date__:   2019/3/31


from recipeInfo import getRecipeInfo
from recipeList import getRecipeList

r_list = getRecipeList()

for index in list(range(r_list)):
    getRecipeInfo(r_list[index][0])