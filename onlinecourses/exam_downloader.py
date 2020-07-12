import os
import requests
from scrapy.selector import Selector
import codecs
from pprint import pprint
import re

username = os.environ['UET_USER']
password = os.environ['UET_PASS']

urls = [
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99686&cmid=1901",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=47370&cmid=1901",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99219&cmid=1901",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99692&cmid=2011",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99667&cmid=2011",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99671&cmid=2011",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99711&cmid=2060",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99713&cmid=2060",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99718&cmid=2060",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99739&cmid=1972",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99744&cmid=1972",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99750&cmid=1972",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99751&cmid=1973",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99755&cmid=1973",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99758&cmid=1973",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99761&cmid=1974",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99762&cmid=1974",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99763&cmid=1974",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99768&cmid=1981",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99771&cmid=1981",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99773&cmid=1981",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99791&cmid=1976",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99793&cmid=1976",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99800&cmid=1976",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99816&cmid=1977",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99821&cmid=1977",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99823&cmid=1977",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99828&cmid=1978",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99834&cmid=1978",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99837&cmid=1978",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99838&cmid=1900",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99844&cmid=1900",
    "https://onlinecourses.uet.vnu.edu.vn/mod/quiz/review.php?attempt=99846&cmid=1900",
]

s = requests.Session()

# login
login_url = "https://onlinecourses.uet.vnu.edu.vn/login/index.php"
r = s.post(login_url, data={'username': username, 'password': password}, allow_redirects=False)
# the server response with 2 MoodleSession tokens, thus we have to choose manually
m = re.findall(r'MoodleSession=([a-z0-9]+)', r.headers['Set-Cookie'])
session_cookie = requests.cookies.create_cookie(domain='onlinecourses.uet.vnu.edu.vn', name='MoodleSession', value=m[1])
s.cookies.set_cookie(session_cookie)

# crawl and save
f = codecs.open('tin1.txt', 'w+', encoding='utf-8')
for url in urls:
    data = s.get(url).text.replace('<a class="autolink" title="Thông báo" href="https://onlinecourses.uet.vnu.edu.vn/mod/forum/view.php?id=17">thông báo</a>', 'thông báo')
    parser = Selector(text=data)

    questions = []
    for question in parser.xpath('//div[@class="qtext"]'):
        questions.append(question.xpath('string(.)').get().replace('\r\n', ' '))

    answers = [] 
    for answer in parser.xpath('//div[@class="rightanswer"]'):
        answers.append(answer.xpath('string(.)').get().replace('\r\n', ' ').replace('Câu trả lời đúng là: ', ''))
    print(len(questions), len(answers))
    final = tuple(zip(questions, answers))
    for q in final:
        f.write(q[0] + ' => ' + q[1] + '\n')
    