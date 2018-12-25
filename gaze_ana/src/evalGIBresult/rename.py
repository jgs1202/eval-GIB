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

participants = ['fujiwara','fukuda','hara','ide','inoue','kawaguchi',\
                'kume','maeda','mizusaki','onda','sato','seto','takada',\
                'takasugi','tomonaga','toyama','ueda','watanabe','yoshida',\
                'yoshihara']
task = ['task1','task2','task3','task4']
#participant = ['kume']
for name in participants:
    for task_num in task:
        child_dir = name + '/' + task_num + '/'
        print(child_dir)
        file_list = sorted(glob.glob(child_dir+'*.csv'), key=numericalSort)

        ind = 0
        for file_name in file_list:
            #print(file_name)
            new_name = name + '_' + task_num + '_' + str(ind) + '.csv'
            print(new_name)
            shutil.move(file_name, child_dir + new_name)
            ind += 1
