import time
from flask import Flask, g, request, make_response, render_template
import hashlib
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    return render_template('templates/index.html')
