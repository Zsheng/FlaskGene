# -*- coding: utf8 -*-

'''
输入需要查询的染色体信息
从数据库中查询出比对结果
'''

import csv
import MySQLdb
import time
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

# mkdir
today = time.strftime("%Y-%m-%d")
if os.path.isdir(today):
    pass
else:
    os.mkdir(today)
os.chdir(today)


class SearchInfo:
    def __init__(self, db):
        self.db = db
        try:
            self.conn = MySQLdb.connect("localhost", "root", "11223344", db, charset='utf8')
            self.cur = self.conn.cursor()
        except MySQLdb.Error, e:
            print "Mysql Error: %d, %s", e.args[0], e.args[1]

    def table(self):
        sql = 'show tables from %s' % self.db
        self.cur.execute(sql)
        tables = self.cur.fetchall()
        return tables

    def info(self, sql):
        self.cur.execute(sql)
        rs = self.cur.fetchall()
        return rs

    def close(self):
        self.conn.close()


class HandleInfo:
    def __init__(self, chr, start, end, variant_type, table):
        self.chr = chr
        self.start = start
        self.end = end
        self.vt = variant_type.lower()
        self.table = table

        if table == 'book':
            self.columns = \
                '`ID`,`Syndrome`,`OMIM`,`Chromo`,`Location`,`Start`,`End`,' \
                '`CNV`,`Gene`,`PUBMED`,`Disease_symptoms`,`Hereditary_mode`,' \
                '`Disease`,`Frequency`, `Source`,`Genome`'
            self.columns_type = ''  # 加入查询变异类型的sql语句中，book表中没有变异类型
        elif table == 'Clingen':
            self.columns = \
                '`ID`, `Chromo`, `Start`, `End`, `Variant_Call_type`, ' \
                '`Validation`, `Clinical_Interpretation`, `Subject_Phenotype`'
            self.columns_type = "`Variant_Call_type` like '%%%s' and " % self.vt
        elif table == 'GRCh37_hg19_variants':
            self.columns = \
                '`ID`, `Chromo`, `Start`, `End`, `variantsubtype`, ' \
                '`pubmedid`, `observedgains`, `observedlosses`, `genes`'
            self.columns_type = ''
        elif table == 'GenemapOmim':
            self.columns = \
                '`Chromo`, `Start`, `End`, `Gene_Symbol`, `MIM_Number`, ' \
                '`Disorders`, `Cytogenetic_Location`, `Genomic_Coordinates`,' \
                ' `Entrez_Gene_ID`'
            self.columns_type = ''
        else:
            self.columns = "`Chromo`, `Start`, `End`"
            self.columns_type = ''

    def handle_sql(self):
        sql = "select %s from %s WHERE `Chromo`= '%s' AND %s " \
              "cast(`Start` AS unsigned INT )<=%s and  " \
              "cast(`End` as unsigned INT )>=%s" \
              % (self.columns, self.table, self.chr,
                 self.columns_type, self.start, self.end)
        # print sql
        return sql

    def get_colums(self):
        return self.columns


def write_data(columns, datas, file_name, flag):
    name = time.strftime("%y%m%d%H%M", time.localtime(time.time()))\
           + file_name + flag + '.csv'
    with open(name, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        # print len(datas)
        spamwriter.writerow(columns)
        for data in datas:
            # print data
            spamwriter.writerow(data)


def search(db, chr, start, end, varianttype, flag):
    s = SearchInfo(db)
    for table in s.table():
        print table[0]
        h = HandleInfo(chr, start, end, varianttype, table[0])
        columns = h.get_colums().replace('`', '').split(',')
        print '-----------'
        write_data(columns, s.info(h.handle_sql()), table[0], flag)


if __name__ == '__main__':
    db = 'dbforsearch'
    # sequance = '13:90997311-94281707'
    # varianttype = 'LOSS'

    if len(sys.argv) > 1:
        sequance = sys.argv[1]
        varianttype = sys.argv[-1]
        flag = ''
        chr = str(sequance.split(':')[0])
        start = int(sequance.split(':')[1].split('-')[0])
        end = int(sequance.split(':')[1].split('-')[1])
        search(db, chr, start, end, varianttype, flag)
        y_n = raw_input('继续查询扩增1.5倍后结果？（y or n）').lower()
        if y_n == 'y':
            flag = '_big'
            big_start = str((2 * start) / 3)
            big_end = str((3 * end) / 2)
            search(db, chr, big_start, big_end, varianttype, flag)
        else:
            pass
        print 'Finish!'
    else:
        print 'python search.py 13:90997311-94281707 - loss'
