import urllib.parse as urllib
import requests
import sys
import logging
import http.client
from scrapy import Selector

# For debug
# http.client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

USERNAME = "guest"
PASSWORD = "guest"

login_url = "https://courses.uet.vnu.edu.vn/login/index.php"
course_url = 'https://courses.uet.vnu.edu.vn/course/view.php?id={}'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

ses = requests.Session()

r = ses.get(login_url, headers=headers)
sel = Selector(text=r.text)

# LOGINTOKEN = sel.xpath('//input[@name="logintoken"]/@value').extract()[0]

data = {
    'username': USERNAME,
    'password': PASSWORD,
}

r = ses.post(login_url, data=data, headers=headers)

start = int(sys.argv[1])
end = int(sys.argv[2])

for i in range(start, end):
    r = ses.get(course_url.format(i))
    sel = Selector(text=r.text)
    class_name = sel.xpath('//h1/text()').get()
    print(i, class_name)
