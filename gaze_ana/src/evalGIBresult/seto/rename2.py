# -*- coding: utf-8 -*-
import os
import datetime
import shutil
import glob
import re
def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

child_dir = 'task1/'
file_list = sorted(glob.glob('task1/*.csv'), key=numericalSort)

ind = 0
for file_name in file_list:
    #print(file_name)
    new_name = 'kawaguchi_task1_' + str(ind) + '.csv'
    print(new_name)
    shutil.move(file_name, child_dir + new_name)
    ind += 1
