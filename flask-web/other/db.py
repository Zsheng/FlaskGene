# coding=utf-8
import MySQLdb


# 完善不同的用户角色登陆时，有不同的数据库权限（设置不同的数据库登陆用户， 通过usertype控制）
# user用户，只有查询的权限
# doc用户，查询权限以及对病人信息表有插入权限/修改
# lab用户，有查询的权限
# lab超级用户， 所有权限


# 每个用户的用户名是唯一的
# 病人可以通过身份证号以及手机号查询到自己的检测进度
# 中文乱码问题


class MysqlInfo:
    def __init__(self):
        try:
            self.conn = MySQLdb.connect("127.0.0.1", "root", "11223344", "flask-web", charset='utf8')
            self.cur = self.conn.cursor()
        except MySQLdb.Error, e:
            print("Mysql Error: %d: %s" % (e.args[0], e.args[1]))

    def search_fetchall(self, sql):
        count = 0
        try:
            self.cur.execute(sql)
            r = self.cur.fetchall()
            for data in r:
                count += 1
            if count != 0:
                return r
            else:
                return False
        except MySQLdb.Error, e:
            error_msg = "Mysql Error: %d: %s" % (e.args[0], e.args[1])
            if error_msg:
                print error_msg
                return False

    def search_fetchone(self, sql):
        count = 0
        try:
            self.cur.execute(sql)
            r = self.cur.fetchone()
            for data in r:
                count += 1
            if count != 0:
                return r
            else:
                return False
        except MySQLdb.Error, e:
            error_msg = "Mysql Error: %d: %s" % (e.args[0], e.args[1])
            if error_msg:
                print error_msg
                return False

    def insert_commit(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except MySQLdb.Error, e:
            error_msg = "Mysql Error: %d: %s" % (e.args[0], e.args[1])
            print error_msg
            return False
        return True

    # 完善了信息后，名字也更改
    def alter_user(self, name):
        sql = "update user set `name` = '%s'" % name
        print sql
        return self.insert_commit(sql)

    # 插入新用户
    def insert_user(self, username, password, usertype, email, yanzheng):
        sql = "insert into `user`(`name`, `password`, `usertype`) " \
              "VALUES ( '%s', '%s' , '%s')" % (username, password, usertype)
        self.insert_commit(sql)

        if usertype == '1':
            sql1 = "insert into `t_docinfo`(`t_dname`, `t_demail`, `t_dyanzheng`) VALUES ('%s', '%s', '%s')" % (username, email, yanzheng)
        elif usertype == '3':
            sql1 = "insert into `t_labinfo`(`l_name`, `l_email`) VALUES ('%s', '%s')" % (username, email)
        else:
            return False
        self.insert_commit(sql1)
        return True

    # 查询基因
    def search_gene(self, s_info):
        sql = "select * from t_gene_info WHERE ID = %s" % s_info
        print sql
        # self.cur.execute(sql)
        # return self.cur.fetchall()
        return self.search_fetchall(sql)

    # 查询染色体
    def search_chromo(self, s_info):
        sql = "select * from t_gene_info where Chromo = '%s' limit 10;" % s_info
        print sql
        # self.cur.execute(sql)
        return self.search_fetchall(sql)

    # 查询起始终止位点
    def search_s_e(self, s_info):
        start = s_info.split('-')[0]
        end = s_info.split('-')[0]

        sql = "select * from t_gene_info where 'Start' = '%s' or 'End' = '%s'" % (start, end)
        print sql
        # self.cur.execute(sql)
        return self.search_fetchall(sql)

    # 登录
    def login(self, username, password, usertype):
        # 没有进行检测的用户是无法登陆的（即用户类型为1、3）
        if usertype == '2':
            sql = "select `p_name` from t_patient_info WHERE p_phone='%s' and p_password='%s'" \
                  % (username, password)
        else:
            sql = "select `name` from user WHERE name='%s' and password='%s' and usertype = '%s'" \
                  % (username, password, usertype)
        print sql
        r = self.search_fetchall(sql)
        return r

    # 获得用户类型
    def user_type(self, username):
        sql = "select usertype from user where name = '%s'" % username
        self.cur.execute(sql)
        r = self.search_fetchall(sql)
        return r[0][0]

    # 医生为插入病人信息
    def insert_patient_info(self, p_name, p_sex, p_age, p_idcaed, p_address, p_phone, p_e_name, p_e_phone):
        p_password = p_idcaed[-6:]
        sql = "insert into `t_patient_info`" \
              "(`p_name`, `p_sex`, `p_age`, `p_idcard`, `p_address`, `p_phone`, `p_e_name`, `p_e_phone`, `p_password`, " \
              "`p_zhuantai`, `p_backup`) " \
              "VALUE ( '%s', '%s' , '%s', '%s', '%s', '%s', '%s' , '%s', '%s', 0, 0)" \
              % (p_name, p_sex, p_age, p_idcaed, p_address, p_phone, p_e_name, p_e_phone, p_password)
        print sql
        return self.insert_commit(sql)

    # 插入验证码信息
    def insert_barcode(self, barcode, name):
        sql = "update t_patient_info SET `p_barcode` = '%s' WHERE p_name = '%s'" % (barcode, name)
        print sql
        return self.insert_commit(sql)

    # 确认医生是否为验证
    def doc_yanzhen(self, d_id):
        sql = "select t_dyanzheng from t_docinfo where t_dinfoid = '%s'" % d_id
        self.cur.execute(sql)
        r = self.cur.fetchone()
        print r
        return 1

    # 医生修改个人信息
    def doc_alter(self, d_name, d_email, d_yiyuan, d_zhichen, d_phone, d_keshi, d_yanzheng):
        sql = "update t_docinfo set t_demail='%s', t_dyiyuan='%s', t_dzhichen='%s'," \
              " t_dphone='%s', t_keshi='%s', t_dyanzheng='%s' WHERE t_dname='%s'" \
              % (d_email, d_yiyuan, d_zhichen, d_phone, d_keshi, d_yanzheng, d_name)
        return self.insert_commit(sql)

    # 查询医生的基本信息
    def search_doc_info(self, d_name):
        sql = "select * from t_docinfo where t_dname = '%s'" % d_name
        self.cur.execute(sql)
        r = self.cur.fetchall()
        print sql
        return r

    # user修改个人信息
    def user_alter_info(self, p_name, p_email, p_add, p_phone):
        sql = "update t_patient_info set p_email='%s', p_address='%s', p_phone='%s' WHERE p_name='%s'" \
              % (p_email, p_add, p_phone, p_name)
        print sql
        return self.insert_commit(sql)

    # user查询基本信息.
    def search_user_info(self, p_name):
        sql = "select * from t_patient_info where `p_name` = '%s'" % p_name
        self.cur.execute(sql)
        r = self.cur.fetchall()
        print sql
        return r

    # 通过p_phone获得p_name
    def get_p_name(self, p_phone):
        sql = "select `p_name` from t_patient_info WHERE `p_phone` = '%s'" % p_phone
        return self.search_fetchall(sql)[0][0]

    # lab 修改个人信息
    def lab_alter_info(self, l_name, l_shiyanshi, l_zhize, l_phone, l_email):
        sql = "update t_labinfo set l_shiyanshi='%s', l_zhize='%s', l_phone='%s', l_email='%s' WHERE l_name='%s'" \
              % (l_shiyanshi, l_zhize, l_phone, l_email, l_name)
        print sql
        return self.insert_commit(sql)

    # lab查询基本信息
    def search_lab_info(self, l_name):
        sql = "select * from t_labinfo where l_name = '%s'" % l_name
        self.cur.execute(sql)
        r = self.cur.fetchall()
        return r

    # 记录用户的比对序列
    def chech_seq(self, c_name, c_seq1, c_seq2, c_time, c_value):
        sql = "insert into t_checkseq(`c_name`,`c_seq1`,`c_seq2`,`c_time`,`c_value`) " \
              "value('%s', '%s', '%s', '%s', '%s')" % (c_name, c_seq1, c_seq2, c_time, c_value)
        return self.insert_commit(sql)

    # 查询用户对比序列
    def search_user_seq(self):
        sql = "select * from t_checkseq order by `seq_id` desc limit 8;"
        return self.search_fetchall(sql)

    # 显示实验人员界面的结果
    def lab_search(self):
        sql = "select * from t_sample_info;"
        return self.search_fetchall(sql)

    # 实验人员查询所有的结果
    def lab_search_all(self, info):
        sql = "select * from t_sample_info WHERE p_s_bianhao = '%s' or p_s_name = '%s' or p_s_date = '%s' " \
              " or p_s_from = '%s' or p_s_type = '%s' or p_s_location = '%s'" \
              " or p_s_labtor = '%s' or p_s_state = '%s' " % (
                  info, info, info, info, info, info, info, info)
        print sql
        self.cur.execute(sql)
        return self.cur.fetchall()

    # 实验人员接受样品的信息
    def lab_jieshou(self):
        sql = "select * from `t_patient_info` WHERE `p_zhuantai` = '0'"
        return self.search_fetchall(sql)

    # 实验人员修改样品状态
    def lab_sample_statu(self, statu, backup, p_id):
        sql = "update `t_patient_info` SET `p_zhuantai` = '%s' ,`p_backup` = '%s' where `p_id` = '%s'" \
              % (statu, backup, p_id)
        print sql

        return self.insert_commit(sql)

    # 接收样品，添加信息到表
    def lab_sample_info(self, name, bianhao, date, sample_from, sample_type, location, labtor, p_s_result, p_s_state):
        sql = "insert into `t_sample_info` SET p_s_name = '%s' ,p_s_bianhao = '%s', p_s_date = '%s' " \
              " , p_s_from = '%s' , p_s_type = '%s' , p_s_location = '%s'" \
              " , p_s_labtor = '%s', p_s_result = '%s', p_s_state = '%s'" \
              % (name, bianhao, date, sample_from, sample_type, location, labtor, p_s_result, p_s_state)
        print sql
        return self.insert_commit(sql)

    # 用户查询检测进度等
    def report(self, p_name):
        sql = "select * from t_sample_info WHERE p_s_bianhao = " \
              "(SELECT `p_id` from t_patient_info WHERE `p_name` = '%s')" % p_name
        print sql
        return self.search_fetchall(sql)

    # 查询新闻
    def get_news(self):
        sql = "select `title` from t_news limit 5"
        return self.search_fetchall(sql)

    # 添加新闻
    def add_news(self, title, info):
        sql = "insert into t_news SET `title` = '%s', `info` = '%s'" % (title, info)
        return self.insert_commit(sql)

    def test(self):
        sql = "insert into test(`name`) value('叶');"
        print sql
        return self.insert_commit(sql)


if __name__ == '__main__':
    test = MysqlInfo()
    test.test()
