import requests
import os
import sys
from pprint import pprint

TARGET = 271

URL = "http://dangkyhoc.vnu.edu.vn/dang-nhap/"
URL_PICK = f"http://dangkyhoc.vnu.edu.vn/chon-mon-hoc/{TARGET}/1/1"
URL_LIST = "http://dangkyhoc.vnu.edu.vn/danh-sach-mon-hoc/1/1"
URL_FIN = "http://dangkyhoc.vnu.edu.vn/xac-nhan-dang-ky/1"

CSRF_1 = "Bx1tfbILleOSxmTmKVL7WRAn-hxweyUf44kSUtjXShMkipaWGrHnpl5ipb6RxHDGdBh-tgQnii0bqbFzscdO80AuB4s1"
CORS_2 = "cP9Q5HM_m1WeS0umvbInUJUkQiVFO95phgxli1cln_J7C7cSnmxZcNCWGtY2_uOCE_RyVJA5tguT7AgYaG9Gc8u69CU1"
USERNAME = os.environ['UET_USER']
PASSWORD = os.environ['UET_PASS']

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

cookies = {
    "__RequestVerificationToken": CSRF_1
}

form_body = {
    "LoginName": USERNAME,
    "Password": PASSWORD,
    "__RequestVerificationToken": CORS_2
}

ses = requests.Session()
requests.utils.add_dict_to_cookiejar(ses.cookies, cookies)
response = ses.post(URL, data=form_body, headers=headers, cookies=cookies)
# response = ses.post(URL_LIST)
# response = ses.post(URL_PICK)
# response = ses.post(URL_FIN)
print(response.status_code)
print(response.text[:200])

with open("resp.html", 'w+', encoding="utf-8") as f:
    f.write(response.text)