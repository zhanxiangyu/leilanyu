# -*- coding: utf-8 -*-
import os
import hmac
import hashlib
from flask import Flask, request

app = Flask(__name__)
GITHUB_WEBHOOK_SECRET = ''  # git项目Secret
root_path = '/home/leilanyu/'  # 你的项目路径


@app.route('/my_webhook/', methods=['POST', ])
def webhook():
    for k, v in request.headers.items():
        print k, v

    verify_signature = request.headers.get('X-Hub-Signature')
    sha_name, signature = verify_signature.split('=')
    if sha_name != 'sha1':
        return 'Signature name not sha1', 501

    local_signature = hmac.new(GITHUB_WEBHOOK_SECRET, msg=request.get_data(), digestmod=hashlib.sha1).hexdigest()

    if signature != local_signature:
        return "Signature is not right", 400

    cmd = '/bin/sh {root_path}config/git_web_hook_update.sh &'.format(root_path=root_path)
    code = os.system(cmd)
    if code == 0:
        return 'shell success', 200
    else:
        return 'shell faile', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0')
