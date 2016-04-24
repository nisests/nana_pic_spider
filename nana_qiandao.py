#!usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Nisests'

import requests
import json
import logging
from bs4 import BeautifulSoup
from urllib.parse import unquote

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Host': 'nanabt.com',
    'Origin': 'http://nanabt.com',
    'Referer': 'http://nanabt.com/index.php?m=u&c=login',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

pre_login_url = 'http://nanabt.com/index.php?m=u&c=login'
login_url = 'http://nanabt.com/index.php?m=u&c=login&a=dorun'
coin_url = 'http://nanabt.com/index.php?m=space&c=punch&a=punch'


def login(username, password):
    s = requests.session()
    # 获取csrf
    csrf_content = s.get(pre_login_url, headers=headers)
    csrf_soup = BeautifulSoup(csrf_content.text, 'html.parser')
    csrf = csrf_soup.find("input", attrs={"name": "csrf_token"})['value']
    # print(csrf)

    # 登录
    data = {
        'username': username,
        'password': password,
        'backurl': 'http://nanabt.com/',
        'invite': '',
        'csrf_token': csrf
    }
    login_content = s.post(login_url, headers=headers, data=data)
    login_json = login_content.json()
    last_login_url = unquote(login_json['referer'])
    s.get(last_login_url, headers=headers)
    # print(last_login_url)

    # 签到
    qd_data = {
        'csrf_token': csrf
    }
    qiandao = s.post(coin_url, headers=headers, data=qd_data)
    result = qiandao.json()
    # print(result)
    if result['state'] == 'success':
        logging.warning(username + '获得了' + result['data']['reward'])
    if result['state'] == 'fail':
        logging.warning(username + qiandao.json()['message'][0])


if __name__ == '__main__':
    logging.basicConfig(filename='nana_qiandao.log', level=logging.WARNING, format='%(asctime)s %(message)s')
    with open('nana_info.json', 'r', encoding='utf8') as f:
        nana_info = json.loads(f.read())
    # print(nana_info)
    for username, password in nana_info.items():
        login(username, password)
