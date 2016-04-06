#!/usr/bin/env python3
# -.- coding=utf-8 -.-
__author__ = 'Nisests'

import urllib.request
import re,os

targetDir = r'.\pic'

def destFile(link):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    names = link.split('/')
    name = names[-1]
    path = os.path.join(targetDir,name)
    return path


if __name__ == '__main__':
    weburl = input('请输入nana地址:')
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=weburl,headers=headers)
    webpage = urllib.request.urlopen(req)
    contentBytes = webpage.read()
    # print(contentBytes.decode('utf-8'))
    # for link,t in set(re.findall(r'(http://[^\s]*?(jpg|png|gif))',str(contentBytes))):
    for link,t in set(re.findall(r'(http://172.31.1.18/att/attachment/\d+/thread/.*?(jpg|png|gif))',str(contentBytes))):
        print(link)
        try:
            urllib.request.urlretrieve(link,destFile(link))
        except Exception as e:
            print('失败',e)