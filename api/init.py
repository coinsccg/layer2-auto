# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_cors import CORS

log = None
client = None

def create_app():
    # APP应用
    app = Flask(__name__)

    # 允许跨域
    CORS(app, supports_credentials=True)

    # 允许输出中文
    app.config["JSON_AS_ASCII"] = False
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

    # 生成密钥 base64.b64encode(os.urandom(64)).decode()
    # SECRET_KEY = "p7nHRvtLdwW07sQBoh/p9EBmHXv9DAcutk2vlj4MdSPNgFeTobUVJ3Ss\
    # 2Wwl3T3tuv/ctTpPw+nQKMafU3MRJQ=="
    # app.secret_key = SECRET_KEY

    # 允许上传的文件类型
    # ALLOWED_EXTENSIONS = ["txt", "pdf", "png", "jpg", "jpeg", "gif", "mp3",
    # \"svg", "avi", "mov", "rmvb", "rm", "flv", "mp4", "3gp", "asf", "asx"]

    global log
    global client

    # 本地数据库连接


    # 蓝图注册
    from router import wallet_router

    # app
    app.register_blueprint(wallet_router)

    return app
