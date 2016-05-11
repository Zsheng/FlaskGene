#!-*- coding:utf8 -*-
import os

import qrcode
import time


class Code:
    def __init__(self):
        self.now = time.time()

    # 生成二维码
    def qr_code(self, info):
        info = str(self.now).replace('.', '') + info[-4:]
        path = os.getcwd()+"\\static\\barcode"
        # path = "C:\Users\PC_yesheng.zhang\Desktop\Flask_new_v3.9\\flask-web\\barcode"  # 生成的二维码保存路径
        qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1
        )
        qr.add_data(info)
        qr.make(fit=True)
        img = qr.make_image()
        name = "%s\%s.png" % (path, info)
        img.save(name)
        print "barcode：%s" % info
        return info

    # 解析二维码信息,传入时间戳，转换成时间
    def read_info(self):
        x = time.localtime(self)
        now = time.strftime('%Y-%m-%d %H:%M:%S', x)
        print "解析：", now
        return now


if __name__ == '__main__':
    info = raw_input("input a string: ")
    code_new = Code()
    code_new.qr_code(info)
