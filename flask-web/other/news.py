# coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import re


def get_news():
    url = "http://www.ascendgene.com/index.php?g=home&m=article&a=index&id=14"
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    h3 = soup.find_all('div')
    # all_h3 = []
    # for h in h3:
    #     dd = re.compile(r'<[^>]+>', re.S).sub('', str(h))
    #     all_h3.append(dd)
    return h3


def aa():
    html = '<a href="http://www.jb51.net">脚本之家</a>,Python学习！'
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', html)
    print(dd)


if __name__ == '__main__':
    print get_news()
