import requests
import os
import sys
from scrapy import Selector
from pprint import pprint

# # debug
# import logging
# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

URL_LOGIN = "http://dangkyhoc.vnu.edu.vn/dang-nhap/"
URL_PICK = "http://dangkyhoc.vnu.edu.vn/chon-mon-hoc/{}/1/1"
URL_LIST = "http://dangkyhoc.vnu.edu.vn/danh-sach-mon-hoc/1"
URL_LIST_REGISTERED = "http://dangkyhoc.vnu.edu.vn/danh-sach-mon-hoc-da-dang-ky/1"
URL_FIN = "http://dangkyhoc.vnu.edu.vn/xac-nhan-dang-ky/1"

CSRF_1 = "Bx1tfbILleOSxmTmKVL7WRAn-hxweyUf44kSUtjXShMkipaWGrHnpl5ipb6RxHDGdBh-tgQnii0bqbFzscdO80AuB4s1"
CSRF_2 = "cP9Q5HM_m1WeS0umvbInUJUkQiVFO95phgxli1cln_J7C7cSnmxZcNCWGtY2_uOCE_RyVJA5tguT7AgYaG9Gc8u69CU1"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
}

cookies = {
    "__RequestVerificationToken": CSRF_1,
}

form_body = {
    "LoginName": "",
    "Password": "",
    "__RequestVerificationToken": CSRF_2
}

post_header = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
}

accounts = []
with open('accounts.txt', 'r') as f:
    try:
        data = f.readlines()
        accounts = map(lambda x: x.strip().split(':'), data)
    except Exception as e:
        print('error occured while reading accounts.txt')
        print(e)
        exit(1)

for account in accounts:
    print(f'-------------- {account[0]}:{account[1]} --------------')
    try:
        status_code = 503
        ses = requests.Session()
        requests.utils.add_dict_to_cookiejar(ses.cookies, cookies)
        form_body['LoginName'] = account[0]
        form_body['Password'] = account[1]
        while status_code != 200:
            response = ses.post(URL_LOGIN, data=form_body,
                                headers=headers, cookies=cookies)
            status_code = response.status_code
        status_code = 503

        while status_code != 200:
            response = ses.post(URL_LIST_REGISTERED, headers=post_header)
            status_code = response.status_code
        parser = Selector(text=response.text)
        classes = parser.xpath('//tr')

        count = 1
        for c in classes:
            td = c.xpath('td')
            subject_name = td[1].xpath('./text()').get()
            subject_code = td[3].xpath('./text()').get()
            subject_lecturer = td[4].xpath('./text()').get()
            subject_schedule = td[5].xpath('string(.)').get().strip()
            print("{0:>2}) {1:<12} | {2} - {3} - {4}".format(count, subject_code, subject_schedule, subject_lecturer, subject_name))
            count += 1
        del ses
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        break
