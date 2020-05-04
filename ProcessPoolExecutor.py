#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import time
import fire
from concurrent.futures import ProcessPoolExecutor, wait
from urllib import request


def weakfilescan(url):
    # 多进程调用urlopen，进程会堵塞
    # code = request.urlopen(url).getcode()
    # print(code)
    # 如果啥都不调用，啥都OK
    print('OK')


def run(process_num, *filename):  # 输入多个n值，分成多个子任务来计算结果
    # 实例化进程池，process_num个进程
    executor = ProcessPoolExecutor(process_num)
    start = time.time()
    fs = []  # future列表
    print(filename[0])
    with open(filename[0], 'r') as f:
        for each_line in f.readlines():
            fs.append(executor.submit(weakfilescan, each_line.replace(os.linesep, '')))
    wait(fs)  # 等待计算结束
    end = time.time()
    duration = end - start
    print("total cost: %.2fs" % duration)
    executor.shutdown()  # 销毁进程池


if __name__ == '__main__':
    fire.Fire(run)