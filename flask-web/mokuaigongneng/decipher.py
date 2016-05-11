#  -*- coding: utf-8 -*-
# !/usr/bin/python
import requests
import re
from bs4 import BeautifulSoup
import time
import csv


def get_decipher_id(Chromo_S_E):
    url = 'https://decipher.sanger.ac.uk/search/consented-patients'
    filt = '{"value":[{"value":"' + Chromo_S_E + '","cmp":"overlaps","position":"' + Chromo_S_E + '","field":"position"}],"cmp":"and"}'
    # print filt
    data1 = {
        'xsrf_token': 'zhang',
        'filter': filt
    }

    headers = {
        'Host': 'decipher.sanger.ac.uk',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'x-decipher-layout': 'ajax',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER',
        'Origin': 'https://decipher.sanger.ac.uk',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://decipher.sanger.ac.uk/search?q=missense_variant',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'decipher.session=474351122666237695153848105062871088; PSGI-XSRF-Token=zhang; _pk_id..c02c=bfd1d11faf1cc611.1455526255.1.1455526650.1455526255.; _pk_ses..c02c=*'
    }

    r = requests.post(url=url, headers=headers, data=data1)
    print r.status_code
    # print r.text
    all_id = re.findall('<td>(.\d*?)</td>', r.text)

    print all_id
    return all_id


def get_table(decipher_id):
    list_info = []
    url = 'https://decipher.sanger.ac.uk/patient/%s/cnvs' % decipher_id
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    # csvout = csv.writer(sys.stdout)
    for table in soup.findAll('table'):
        print 'names: ' + ','.join([tr.get_text() for tr in table.findAll('th')])
        for row in table.findAll('tr'):
            #  csvout.writerow([tr.get_text() for tr in row.findAll('td')])
            info = 'info:' + ','.join([tr.get_text().replace("\n", "") for tr in row.findAll('td')])
            print info
            list_info.append(info)
    return list_info


def search(cse):
    keys = get_decipher_id(cse)
    all_info = []
    for key in keys:
        print "Decipher ID: ", key
        info = get_table(key)
        print '**************************************'
        time.sleep(2)
        all_info.append(info)
    return all_info


def write_data(names, datas, file_name):
    names = names.split(',')
    with open(file_name + '.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(names)
        # print datas
        for data in datas:
            for one_data in data:
                # print one_data
                spamwriter.writerow(one_data.split(','))


if __name__ == '__main__':
    # cse = '13:30805425-36900741'
    cse = raw_input('输入序列(13:30805425-36900741):')
    list_all = search(cse)
    print list_all
    if raw_input('导出csv文件？').lower() == 'y':
        names = 'Location,Size,Mean Ratio,Genes,Inheritance,PathogenicityContribution?,DS Score /Sampling Probability?,Links'
        file_name = cse
        write_data(names, list_all, file_name)
        print '导出成功！'
    else:
        print '查询结束。'
