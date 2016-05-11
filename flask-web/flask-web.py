# coding=utf-8
from flask import Flask, render_template, session, redirect, url_for, flash, request, escape, make_response, Response, \
    send_from_directory, Blueprint
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.paginate import Pagination
# from flask.ext.mail import Mail
import os
import time

from werkzeug.utils import secure_filename

from db import MysqlInfo
from models import *
from barcode import Code  # 生产二维码
from uploadfile import allowed_file
from nwDistance import NWDistance
from send_email import send_mail

# create_engine('mysql+mysqldb://USER:@SERVER:PORT/DB?charset=utf8', encoding='utf-8')
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SECRET_KEY'] = 'hard to get string'
# app.config['MAIL_SERVER'] = 'smpt.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# mail = Mail(app)

app = Flask(__name__)

CSRF_ENABLED = True

# Flask-WTF能保护所有表单面免受跨站请求伪造（Cross-Site Request Forgery，CSRF）的攻击
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
handel_db = MysqlInfo()

UPLOAD_FOLDER = 'static/upload'


def add_cookie(ut):
    if ut:
        usertype = str(handel_db.user_type(session['username']))
    else:
        usertype = '2'
    res = Response(render_template('index.html'))
    res.set_cookie(key='usertype', value=usertype)
    return res


@app.route('/')
def index():
    # newssearch = NewsSearch(request.form)
    # news = get_news('基因检测')
    news = ['产业巨头代表聚首IVD：探讨“NIPT在中国”', '基因+人工智能，Deep Genomics将会把精准医疗带往何处？']
    if 'username' in session:
        return render_template('index.html', name=session['username'], news=news)
    session['username'] = ''
    return render_template('index.html', name=False, news=news)
    # return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        handel_db.insert_user(form.username.data, form.password.data, form.usertype.data, form.email.data, yanzheng=0)
        # db_session.add(user)
        session['username'] = request.form['username']
        flash('Thanks for registering')

        res = Response(render_template('index.html'))
        res.set_cookie(key='usertype', value=form.usertype.data)
        return res
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    log_form = LoginForm(request.form)
    msg = False
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        usertype = request.form['usertype']

        # if handel_db.quanxian()

        if handel_db.login(username, pwd, usertype):
            if usertype == '2':
                session['username'] = handel_db.get_p_name(username)
                ut = False
            else:
                session['username'] = request.form['username']
                ut = True
            return add_cookie(ut)
        else:
            msg = True
    return render_template('login.html', form=log_form, msg=msg)


@app.route('/logout')
def logout():
    # print "前：", session['username']
    session.pop('username', None)
    # print "后：", session['username']
    res = make_response(redirect(url_for('index')))
    res.set_cookie('usertype', '', expires=0)
    return res


@app.route("/base")
def base():
    return render_template("base.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_erro(e):
    return render_template('500.html'), 500


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    sForm = SearchGeneInfo(request.form)
    show_info = None
    if request.method == 'POST':
        s_info = request.form['search']
        s_type = request.form['search_type']
        if s_type == '1':
            show_info = handel_db.search_gene(s_info)
        elif s_type == '2':
            show_info = handel_db.search_chromo(s_info)
        elif s_type == '3':
            show_info = handel_db.search_s_e(s_info)
        else:
            show_info = False
        return render_template('search.html', show_info=show_info, form=sForm, lenght=len(show_info))
    return render_template('search.html', form=sForm, show_info=show_info)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'GET':
        return render_template('check.html')
    elif request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)   # 获取一个安全的文件名，且仅仅支持ascii字符；
        f.save(os.path.join(UPLOAD_FOLDER, fname))
        return '上传成功'


@app.route('/check', methods=['POST', 'GET'])
def check():
    check_form = CheckForm(request.form)
    seq_form = SeqForm(request.form)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file'))
    return render_template('check.html', form=check_form, seq_form=seq_form)


@app.route('/seqcheck', methods=['POST', 'GET'])
def seqcheck():
    seq1 = str(request.form['seq1'])
    seq2 = str(request.form['seq2'])
    value = NWDistance(seq1, seq2)
    c_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if session['username'] != '':
        c_name = session['username']
    else:
        c_name = 'Stanger'
    handel_db.chech_seq(c_name, seq1, seq2, c_time, value)
    info = handel_db.search_user_seq()
    return render_template('success_check.html', value=value, seq1=seq1, seq2=seq2, info=info, c_time=c_time)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/doc', methods=['GET', 'POST'])
def doc_index():
    if request.cookies.get('usertype') != '1':
        return redirect(url_for('logout'))
    docForm = DocPatientInfo(request.form)
    username = session['username']  # 查询使用的用户名，最终确定为登陆网站的唯一用户名，采用session['username']赋值
    info = handel_db.search_doc_info(username)
    if request.method == 'POST':
        # 预约，病人信息数据到数据库
        p_name = request.form['p_name']
        p_sex = request.form['p_sex']
        p_age = request.form['p_age']
        p_idcard = request.form['p_idcard']
        p_address = request.form['p_address']
        p_phone = request.form['p_phone']
        p_emergency_contact = request.form['p_emergency_contact']
        p_emergency_phone = request.form['P_emergency_phone']
        if handel_db.insert_patient_info(p_name, p_sex, p_age,  p_idcard, p_address,
                                         p_phone, p_emergency_contact, p_emergency_phone):
            # 生成二维码，再插入到数据库/显示在网页上！
            c = Code()
            code_name = c.qr_code(str(p_idcard))+'.png'
            handel_db.insert_barcode(code_name, p_name)
            return render_template('barcode.html', code_name=code_name)
        else:
            msg = "请确认信息后输入！"
            flash(msg)
            return render_template('index_doc.html', form=docForm)
    return render_template('index_doc.html', form=docForm, info=info)


@app.route('/user', methods=['GET', 'POST'])
def user_index():
    if request.cookies.get('usertype') != '2':
        return redirect(url_for('logout'))
    username = session['username']  # 查询使用的用户名，最终确定为登陆网站的唯一用户名，采用session['username']赋值
    info = handel_db.search_user_info(username)
    # 查询报告的检测进度
    rep_info = handel_db.report(username)
    print rep_info
    return render_template('index_user.html', info=info, rep_info=rep_info, length=len(rep_info))


@app.route('/lab', methods=['GET', 'POST'])
def lab_index():
    form = SearchPatientInfo(request.form)
    if request.cookies.get('usertype') != '3':
        return redirect(url_for('logout'))

    username = session['username']
    info = handel_db.search_lab_info(username)
    results = handel_db.lab_search()
    if request.method == 'POST':
        results = handel_db.lab_search_all(request.form['search'])
    return render_template('index_lab.html', form=form, info=info, results=results, length=len(results))


@app.route('/doc_alter_info', methods=['GET', 'POST'])
def doc_alter_info():
    form = DocInfoAlter(request.form)
    if request.method == 'POST':
        d_name = session['username']
        d_email = request.form['d_email']
        d_yiyuan = request.form['d_yiyuan']
        d_zhichen = request.form['d_zhichen']
        d_phone = request.form['d_phone']
        d_keshi = request.form['d_keshi']
        doc_id = 1  # 这个ID为t_docinfo表中医生对应的t_dinfoid
        if handel_db.doc_yanzhen(doc_id) == 1:
            d_yanzheng = 1
        else:
            d_yanzheng = 0
        handel_db.doc_alter(d_name, d_email, d_yiyuan, d_zhichen, d_phone, d_keshi, d_yanzheng)  # 医生修改信息后插入数据库
        return redirect(url_for('doc_index'))
    return render_template('doc_info_alter.html', form=form)


@app.route('/user_alter_info', methods=['GET', 'POST'])
def user_alter_info():
    form = UserInfoAlter(request.form)
    if request.method == 'POST':
        u_name = session['username']
        u_email = request.form['u_email']
        u_add = request.form['u_add']
        u_phone = request.form['u_phone']
        handel_db.user_alter_info(u_name, u_email, u_add, u_phone)
        return render_template('index.html')
    return render_template('user_info_alter.html', form=form)


@app.route('/lab_alter_info', methods=['POST', 'GET'])
def lab_alter_info():
    form = LabInfoAlter(request.form)
    if request.method == 'POST':
        l_name = session['username']
        l_shiyanshi = request.form['l_shiyanshi']
        l_zhize = request.form['l_zhize']
        l_phone = request.form['l_phone']
        l_email = request.form['l_email']
        handel_db.lab_alter_info(l_name, l_shiyanshi, l_zhize, l_phone, l_email)
        return redirect(url_for('lab_index'))
    return render_template('lab_info_alter.html', form=form)


@app.route('/lab_jieshou', methods=['POST', 'GET'])
def lab_jieshou():
    form = LabJieshouBeifen(request.form)
    info = handel_db.lab_jieshou()
    if info:
        length = len(info)
        p_id = info[0][0]
    else:
        length = 0
        p_id = None

    if request.method == 'POST':
        # 修改样品状态
        handel_db.lab_sample_statu(request.form['jieshou'], request.form['beifen'], p_id)
        # 完善样品信息
        name = request.form['name']
        bianhao = info[0][0]
        date = request.form['date']
        songjian = request.form['songjian']
        yp_type = request.form['yp_type']
        yp_location = request.form['yp_location']
        labtor = str(session['username'])
        p_s_result = "暂无结果"
        p_s_state = "1"
        handel_db.lab_sample_info(name, bianhao, date, songjian, yp_type, yp_location, labtor, p_s_result, p_s_state)

    return render_template('lab_jieshou.html', info=info, length=length, form=form)


@app.route('/report', methods=['POST', 'GET'])
def report():
    p_s_bianhao = ''
    info = handel_db.report(p_s_bianhao)


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('bui-bootstrap/index.html')


if __name__ == '__main__':
    app.run(debug=True)
