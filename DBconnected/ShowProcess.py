# /usr/bin/env python
# -*- coding: utf-8 -*-
# __Author__: yunrui
# __Date__:   2019/4/2
# Last_modified_time: 2019/4/4

import sys
import time

class ShowProcess():
    
    i = 0   #当前处理的进度
    max_steps = 0   #总共要处理的次数
    max_arrow = 50   #进度条的长度
    infoDone = 'done'   #完成时显示的字符串

    def __init__(self, max_steps, infoDone='done'):
        self.max_steps = max_steps
        self.infoDone = infoDone
        self.i = 0
    
    def showProcess(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        
        num_arrow = int(self.i * self.max_arrow / self.max_steps)
        num_line = self.max_arrow - num_arrow
        percent = self.i * 100.00 / self.max_steps
        #闪烁效果
        process_bar = '[' + '#' * (num_arrow+1) + '-' * (num_line-1) + ']' + '%.2f' % percent + '%' + '\r'
        sys.stdout.write(process_bar)
        time.sleep(0.3)
        sys.stdout.flush()
        process_bar = '[' + '#' * num_arrow + '-' * num_line + ']' + '%.2f' % percent + '%' + '\r'
        sys.stdout.write(process_bar)
        sys.stdout.flush()

        if self.i >= self.max_steps:
            self.close()
    
    def close(self):
        print(' ')
        print(self.infoDone)
        self.i = 0

