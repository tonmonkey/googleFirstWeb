# -*- coding: UTF-8 -*-

import requests
import time
import random
from lxml import etree
import urllib3
import threading


banner = """
V1.0.1
   ___                  _        __                     _     
  / _ \___   ___   __ _| | ___  / _\ ___  __ _ _ __ ___| |__  
 / /_\/ _ \ / _ \ / _` | |/ _ \ \ \ / _ \/ _` | '__/ __| '_ \ 
/ /_\\ (_) | (_) | (_| | |  __/ _\ \  __/ (_| | | | (__| | | |
\____/\___/ \___/ \__, |_|\___| \__/\___|\__,_|_|  \___|_| |_|
                  |___/                                       
Tommonkey
"""


# setting proxy
proxies = {
    'http': 'http://localhost:7890',
    'https': 'http://localhost:7890'
}

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    }


def input_data():
    List = []
    with open(r"./target.txt", encoding="utf=8") as f:
        for u in f.readlines():
            u = u.strip("\n")
            List.append(u)
        # print(List)
        return List


# send requests
def requestPackage(i):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        googleUrl = "https://www.google.com/search?q="
        googleUrl = googleUrl + i
        data_Raw = requests.get(url=googleUrl, headers=headers, proxies=proxies, timeout=20, verify=False)
        data_Raw.close()
        time.sleep(random.randint(2, 5))
        print("[+] 正在搜索{}".format(i))
        if data_Raw.status_code == 200:
            print("[+] 回包状态值：{}".format(data_Raw.status_code))
            data_text = data_Raw.text
            # core deal string
            result = etree.HTML(data_text).xpath('//*[@class="tjvcx GvPZzd cHaqb"]/text()')
            if len(result) != 0:
                if "edu" in result[0]:
                    print("[+]" + result[0])
                    with open("result.txt", mode="a+") as fd:
                        fd.write( i+ ":" + result[0] + "\n")
                else:
                    print("[+]" + result[0])
                    with open("fail.txt", mode="a+") as fd:
                        fd.write(result[0] + ":" + i + "\n")
                return 0
            else:
                return 1
    except OSError:
        pass
        return 1


def queryData(list):
    try:
        for i in list:
            status = requestPackage(i)
            if status == 0:
                pass
            else:
                for num in [1,2,3]:
                    print("[+] 发送请求失败,正在重试，重试次数：{}/3".format(num))
                    statusT = requestPackage(i)
                    if statusT == 1:
                        if num == 3:
                            print("[+] 抓取失败，写入NoCapture.txt")
                            with open("NoCapture.txt", mode="a+") as fd:
                                fd.write(i + "\n")
                        continue
                    else:
                        break

    except Exception as err:
        print(err)


if __name__ == "__main__":
    print(banner)
    list = input_data()
    result = queryData(list)
    print(result)
