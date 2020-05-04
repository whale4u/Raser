import os
from concurrent.futures import ThreadPoolExecutor, wait

import requests

# 全局设置
using_dict = './dict/actuator.txt'
threads_count = 4  # 线程数
timeout = 3  # 超时时间
allow_redirects = True  # 是否允许URL重定向
headers = {  # HTTP 头设置
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
    'Referer': 'http://www.google.com',
    'Cookie': 'whoami=raser',
}


# 分割子任务
def each_task(url):
    with open(using_dict, 'r') as suffix_file:
        last_url = ""
        for each_suffix in suffix_file.readlines():
            full_url = '%s/%s' % (url, each_suffix)
            req = requests.get(full_url, stream=True, headers=headers, timeout=timeout, allow_redirects=allow_redirects)
            code = str(req.status_code)
            if "2" in code:
                if last_url != url:
                    last_url = url
                    # print('%s ---> %s' % (req.status_code, full_url))
                    print(full_url, end="")
            # print('%s ---> %s' % (req.status_code, full_url))


def run(thread_num, filename):
    # 实例化线程池，thread_num个线程
    executor = ThreadPoolExecutor(thread_num)
    fs = []  # future列表
    # print(filename)
    with open(filename, 'r') as f:
        for each_line in f.readlines():
            fs.append(executor.submit(each_task, each_line.replace(os.linesep, '')))
    wait(fs)  # 等待计算结束
    executor.shutdown()  # 销毁线程池


if __name__ == '__main__':
    run(thread_num=threads_count, filename="target/pingan.txt")
