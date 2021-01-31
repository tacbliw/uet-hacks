#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import requests
from scrapy.selector import Selector
from pprint import pprint

BASE_URL = 'http://112.137.129.87/qldt/'
CURRENT_TERM_ID = '030'

headers = {
    'User-Agent': 'Mozilla/5.0'
}

class ResultEntry:
    masvTitle = ''
    hotenTitle = ''
    ngaysinhTitle = ''
    lopkhoahocTitle = ''
    tenlopmonhocTitle = ''
    tenmonhocTitle = ''
    nhom = ''
    sotinchiTitle = ''
    ghichu = ''

    def __init__(self, masvTitle=''):
        self.masvTitle = masvTitle

    def __eq__(self, other):
        return self.masvTitle == other.masvTitle and self.tenlopmonhocTitle == other.tenlopmonhocTitle

    def __repr__(self):
        return f"<ResultEntry masv='{self.masvTitle}' hoten='{self.hotenTitle}' lopmonhoc='{self.tenlopmonhocTitle}>'"


def build_payload(masvTitle='', hotenTitle='', ngaysinhTitle='',
                    lopkhoahocTitle='', tenlopmonhocTitle='', tenmonhocTitle='',
                    nhom='', sotinchiTitle='', ghichu='', pageSize=1000, page=1
                ) -> dict:
    payload = {
        'SinhvienLmh[masvTitle]': masvTitle,
        'SinhvienLmh[hotenTitle]': hotenTitle,
        'SinhvienLmh[ngaysinhTitle]': ngaysinhTitle,
        'SinhvienLmh[lopkhoahocTitle]': lopkhoahocTitle,
        'SinhvienLmh[tenlopmonhocTitle]': tenlopmonhocTitle,
        'SinhvienLmh[tenmonhocTitle]': tenmonhocTitle,
        'SinhvienLmh[nhom]': nhom,
        'SinhvienLmh[sotinchiTitle]': sotinchiTitle,
        'SinhvienLmh[ghichu]': ghichu,
        'SinhvienLmh[term_id]': CURRENT_TERM_ID,
        'pageSize': pageSize,
        'page': page,
        'ajax': 'sinhvien-lmh-grid',
    }
    return payload


def parse_resp(resp: str) -> list:
    if 'No result' in resp:
        return []
    parser = Selector(text=resp)
    tr = parser.xpath('//tbody/tr')
    result = []
    for e in tr:
        td = e.xpath('td/text()')

        entry = ResultEntry()
        entry.masvTitle = td[1].get()
        entry.hotenTitle = td[2].get()
        entry.ngaysinhTitle = td[3].get()
        entry.lopkhoahocTitle = td[4].get()
        entry.tenlopmonhocTitle = td[5].get()
        entry.tenmonhocTitle = td[6].get()
        entry.nhom = td[7].get()
        entry.sotinchiTitle = td[8].get()
        entry.ghichu = td[9].get()

        result.append(entry)
    return result


def query(payload: dict) -> [ResultEntry]:
    r = requests.get(BASE_URL, headers=headers, params=payload)
    return parse_resp(r.text)

paths = []
cache = {}

def trace(f1: ResultEntry, me: ResultEntry, path, depth=2):
    if depth <= 0:
        return
    
    print(f"trace {depth}: {path}")
    classes = query(build_payload(masvTitle=f1.masvTitle))
    for c in classes:
        if c.tenlopmonhocTitle in path:
            continue
        participants = query(build_payload(tenlopmonhocTitle=c.tenlopmonhocTitle))
        if any(x.masvTitle == me.masvTitle for x in participants):
            global paths
            current_path = path + (c.tenlopmonhocTitle, me.masvTitle)
            paths.append(current_path)
            continue
        for p in participants:
            trace(p, me, path + (c.tenlopmonhocTitle, p.masvTitle), depth - 1)



if __name__ == '__main__':
    f1 = ResultEntry('18021117')
    me = ResultEntry('18021388')

    try:
        trace(f1, me, (f1.masvTitle,))
    except KeyboardInterrupt:
        pass

    pprint(paths)