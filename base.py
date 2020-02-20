#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import requests
from pprint import pprint

# debug
import logging
import http.client as http_client
http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

USERNAME = os.environ['UET_USER']
PASSWORD = os.environ['UET_PASS']

headers = {
    'User-Agent': 'Mozilla/5.0'
}

cookies = {

}

payload = {

}

s = requests.Session()