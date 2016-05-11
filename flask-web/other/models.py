# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, validators, SelectField,\
    FileField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('Confirm Password', message='Passwords must match')
    ])
    confirm = PasswordField('Config Password', [validators.DataRequired()])
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    usertype = SelectField('UserType', choices=[('1', 'Doctor'), ('2', 'Patient'), ('3', 'Worker')])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=25), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=3, max=35), validators.DataRequired()])
    usertype = SelectField('UserType', choices=[('1', 'Doctor'), ('2', 'Patient'), ('3', 'Worker')])


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchGeneInfo(Form):
    search = StringField('SearchGeneInfo', [validators.DataRequired()])
    search_type = SelectField('SearchType', choices=[('1', 'Gene'), ('2', 'Chromo'), ('3', 'Start-End')])
    # s_type = SelectField('SearchType1', choices=[('1', 'Gene'), ('2', 'Chromo'), ('3', 'Start-End')])


class CheckForm(Form):
    file_form = FileField('Fiel', [validators.DataRequired()])


class DocPatientInfo(Form):
    p_name = StringField('PatientName', [validators.DataRequired()])
    p_sex = SelectField('PatientSex', choices=[('1', 'Male'), ('2', 'Female')])
    p_age = IntegerField('PatientAge', [validators.DataRequired()])
    p_idcard = StringField('PatientID', [validators.DataRequired()])
    p_address = StringField('PatientAddress', [validators.DataRequired()])
    p_phone = IntegerField('PatientPhone', [validators.DataRequired()])
    p_emergency_contact = StringField('PatinetEmergencyContact', [validators.DataRequired()])
    P_emergency_phone = StringField('PatientEmergencyPhone', [validators.DataRequired()])


class DocInfoAlter(Form):
    d_name = StringField('DocName', [validators.DataRequired()])
    d_email = StringField('DocEmail', [validators.DataRequired()])
    d_yiyuan = StringField('DocYiyuan', [validators.DataRequired()])
    d_zhichen = StringField('DocZhichen', [validators.DataRequired()])
    d_phone = IntegerField('DocPhone', [validators.DataRequired()])
    d_keshi = StringField('DocKeshi', [validators.DataRequired()])


class UserInfoAlter(Form):
    u_name = StringField('UserName', [validators.DataRequired()])
    u_email = StringField('UserEmail', [validators.DataRequired()])
    u_add = StringField('UserAddress', [validators.DataRequired()])
    u_phone = IntegerField('UserPhone', [validators.DataRequired()])


class LabInfoAlter(Form):
    l_name = StringField('LabtorName', [validators.DataRequired()])
    l_shiyanshi = StringField('LabShiyanshi', [validators.DataRequired()])
    l_zhize = StringField('LabZhize', [validators.DataRequired()])
    l_phone = StringField('l_phone', [validators.DataRequired()])
    l_email = StringField('l_email', [validators.DataRequired()])


class SeqForm(Form):
    seq1 = TextAreaField('seq1', [validators.DataRequired()])
    seq2 = TextAreaField('seq2', [validators.DataRequired()])


class SearchPatientInfo(Form):
    search = StringField('SearchPatientInfo', [validators.DataRequired()])


class LabJieshouBeifen(Form):
    jieshou = SelectField('jieshou', choices=[('1', 'Yes'), ('0', 'No')])
    beifen = SelectField('beifen', choices=[('1', 'Yes'), ('0', 'No')])

    # bianhao = StringField('bianhao', [validators.DataRequired()])
    name = SelectField('xiangmu', choices=[('1', '无创产前检测'), ('2', '大众基因检测'), ('3', '健康管理报告')])
    date = StringField('date', [validators.DataRequired()])
    songjian = StringField('songjian', [validators.DataRequired()])
    yp_type = SelectField('yp_type', choices=[('1', '绒毛组织'), ('2', '血液'), ('3','唾液')])
    yp_location = SelectField('yp_location', choices=[('1', '-80冰箱'), ('2', '-20冰箱'), ('3','常温')])


class LabXiugai(Form):
    xiugai = RadioField('xiugai', [validators.DataRequired()], choices=[('1', '')], default='1')


class NewsSearch(Form):
    word = StringField('NewsWord', [validators.DataRequired()])