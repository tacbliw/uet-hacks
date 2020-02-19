#!/bin/python
# -*- coding: utf-8 -*-

import requests
import os
from pprint import pprint

# For debug
# import logging
# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1
# 
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

username = os.environ['UET_USER']
password = os.environ['UET_PASS']

URL = "http://oasis.uet.vnu.edu.vn/"
login_path ='api/auth/signin'
ranking_path = 'api/ranking/courses/6?page=0&size=50'


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3",
    "Host": "oasis.uet.vnu.edu.vn",
    "Referer": "http://oasis.uet.vnu.edu.vn/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}

cookies = {}

s = requests.Session()
s.headers.update(headers)

# Login
r = s.post(URL + login_path, json={
    'password': password,
    'username_or_email': username
})
token = r.json()['access_token']
token_type = r.json()['token_type']
s.headers.update({'Authorization': token_type + ' ' + token})

# Call
r = s.get(URL + ranking_path)
studentList = r.json()['content']

print('+' + '-' * 28 + '+')
print("|{0:<20s}|{1:>7s}|".format("Name", "Score"))
print('+' + '-' * 28 + '+')
for student in studentList:
    print("|{0:<20s}|{1:>7d}|".format(student['student_name'], student['score']))
print('+' + '-' * 28 + '+')
