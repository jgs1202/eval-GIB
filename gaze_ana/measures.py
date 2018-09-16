# -*- coding: utf-8 -*-

import math
import os
import csv
import json


def makefile():
    data = [[[] for j in range(120)] for i in range(4)]
    origin = './src/Analyze/'
    outpath = './src/trajectory/'
    srcpath = './src/data/'

    for who in os.listdir(origin):
        if who != '.DS_Store':
            for task in os.listdir(origin + who):
                if task != '.DS_Store':
                    for file in range(120):
                        f = open(origin + who + '/' + task + '/' + str(file) + '.csv', 'r')
                        reader = csv.reader(f)
                        datum = [i for i in reader]
                        f.close()
                        for i in range(len(datum) - 1):
                            dic = {}
                            if type(datum[i][1]) == 'list':
                                datum[i][1] = datum[i][1][0]
                            dic['AOI'], dic['duration'] = datum[i][1], datum[i][4]
                            dic['x'], dic['y'] = datum[i][2], datum[i][3]
                            data[int(task[-1]) - 1][file].append(dic)

    out = [[[] for j in range(120)] for i in range(4)]
    for task in range(len(out)):
        for que in range(len(out[task])):
            answer = json.load(open(srcpath + 'task' + str(int(task) + 1) + '/' + str(que) + '.json'))
            if task == 1:
                if que < 60:
                    ans = answer['nodeMax']
                    ans2 = answer['node2ndMax']
                    ans3 = answer['node3rdMax']
                else:
                    ans = answer['nodeMin']
                    ans2 = answer['node2ndMin']
                    ans3 = answer['node3rdMin']
            if task == 2:
                if que < 60:
                    ans = answer['linkMax']
                    ans2 = answer['link2ndMax']
                    ans3 = answer['link3rdMax']
                else:
                    ans = answer['linkMin']
                    ans2 = answer['link2ndMin']
                    ans3 = answer['link3rdMin']
            if task == 3:
                ans = answer['linkOutMost']
                ans2 = answer['linkOut2nd']
                ans3 = answer['linkOut3rd']
            dic = {}
            dic['layout'] = answer['type']
            dic['total'] = len(data[int(task)][que])
            dic['length'] = 0.
            for i in range(len(data[task][que])):
                if i != len(data[task][que]) - 1:
                    dx = float(data[task][que][i]['x']) - float(data[task][que][i+1]['x'])
                    dy = float(data[task][que][i]['y']) - float(data[task][que][i+1]['y'])
                    dic['length'] += math.sqrt(dx*dx + dy*dy)
            if task != 0:
                totalDur, ansDur, ansCount = 0, 0, 0
                ans2Dur, ans3Dur, ans2Count, ans3Count = 0., 0., 0, 0
                for i in range(len(data[task][que])):
                    totalDur += float(data[task][que][i]['duration'])
                    if ans == int(data[task][que][i]['AOI']) - 1:
                        ansDur += float(data[task][que][i]['duration'])
                        ansCount += 1
                    if ans2 == int(data[task][que][i]['AOI']) - 1:
                        ans2Dur += float(data[task][que][i]['duration'])
                        ans2Count += 1
                    if ans3 == int(data[task][que][i]['AOI']) - 1:
                        ans3Dur += float(data[task][que][i]['duration'])
                        ans3Count += 1
                    elif type(ans) == list:
                        # for an in ans:
                        if ans[0] == int(data[task][que][i]['AOI']) - 1:
                            ansDur += float(data[task][que][i]['duration'])
                            ansCount += 1
                dic['ansDur'] = ansDur
                dic['totalDur'] = totalDur
                dic['ansCount'] = ansCount
                dic['ans2Dur'] = ans2Dur
                dic['ans3Dur'] = ans3Dur
                dic['ans2Count'] = ans2Count
                dic['ans3Count'] = ans3Count
            out[task][que] = dic
    output = [[{} for i in range(4)] for j in range(4)]
    for task in range(4):
        for datum in out[task]:
            if datum['layout'] =='STGIB':
                layout = 0
            elif datum['layout'] =='Chatu':
                layout = 1
            elif datum['layout'] =='FDGIB':
                layout = 2
            elif datum['layout'] =='TRGIB':
                layout = 3
            try:
                output[task][layout]['total']
            except:
                output[task][layout]['total'] = 0
                output[task][layout]['length'] = 0
                output[task][layout]['layout'] = datum['layout']
                if task != 0:
                    output[task][layout]['ansDur'] = 0.
                    output[task][layout]['totalDur'] = 0.
                    output[task][layout]['ansCount'] = 0.
                    output[task][layout]['ans2Dur'] = 0.
                    output[task][layout]['ans2Count'] = 0.
                    output[task][layout]['ans3Dur'] = 0.
                    output[task][layout]['ans3Count'] = 0.
            output[task][layout]['total'] += datum['total']
            output[task][layout]['length'] += datum['length']
            if task != 0:
                output[task][layout]['ansDur'] += datum['ansDur']
                output[task][layout]['totalDur'] += datum['totalDur']
                output[task][layout]['ansCount'] += datum['ansCount']
                output[task][layout]['ans2Dur'] += datum['ans2Dur']
                output[task][layout]['ans2Count'] += datum['ans2Count']
                output[task][layout]['ans3Dur'] += datum['ans3Dur']
                output[task][layout]['ans3Count'] += datum['ans3Count']
    for i in range(4):
        for j in range(4):
            output[i][j]['length'] = output[i][j]['length'] / 120 / 20
            if i != 0:
                output[i][j]['durAnsRatio'] = output[i][j]['ansDur'] / output[i][j]['totalDur']
                output[i][j]['ansCountRatio'] = output[i][j]['ansCount'] / output[i][j]['total']
                output[i][j]['durAns2Ratio'] = output[i][j]['ans2Dur'] / output[i][j]['totalDur']
                output[i][j]['ans2CountRatio'] = output[i][j]['ans2Count'] / output[i][j]['total']
                output[i][j]['durAns3Ratio'] = output[i][j]['ans3Dur'] / output[i][j]['totalDur']
                output[i][j]['ans3CountRatio'] = output[i][j]['ans3Count'] / output[i][j]['total']
    print(output)
    f = open(outpath + 'measure.json', 'w')
    json.dump(output, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def main():
    makefile()


if __name__ == '__main__':
    main()