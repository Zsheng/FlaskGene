import os

basedir = os.path.abspath(os.path.dirname(__file__))


def read_txt(fname):
    f = open(basedir+"\\static\\upload\\"+fname, "r")
    while True:
        line = f.readline()
        if line:
            print line
        else:
            break
    f.close()

read_txt('a')
