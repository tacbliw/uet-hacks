import requests
import os
import logging
import http.client
from scrapy import Selector
from pprint import pprint

# For debug
# http.client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

USERNAME = os.environ['UET_USER']
PASSWORD = os.environ['UET_PASS']

COURSE_ID = 5676
login_page_url = "https://courses.uet.vnu.edu.vn/alternateLogin/index.php"
login_post_url = "https://courses.uet.vnu.edu.vn/login/index.php"
course_url = 'https://courses.uet.vnu.edu.vn/course/view.php?id={}'
resource_url = 'https://courses.uet.vnu.edu.vn/mod/resource/view.php?id={}'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

ses = requests.Session()

# Login
r = ses.get(login_page_url, headers=headers)

# sel = Selector(text=r.text)
# LOGINTOKEN = sel.xpath('//input[@name="logintoken"]/@value').extract()[0]

data = {
    'username': USERNAME,
    'password': PASSWORD,
    # 'logintoken': LOGINTOKEN
}

r = ses.post(login_post_url, data=data, headers=headers)

# Get resource links
r = ses.get(course_url.format(COURSE_ID), headers=headers)
sel = Selector(text=r.text)
resource_path = '//div[@class="activityinstance"]/a/@href'
resources = sel.xpath(resource_path).extract()
for x in resources:
    if 'resource' in x:
        print(x)
