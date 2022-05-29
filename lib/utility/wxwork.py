import base64
import hashlib
import requests
import json
from lib.utility.writelog import log


logger = log()
# url_i = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c2b33853-8d8b-4bd5-b651-ab371192bb35' #测试url
url_i = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2124a91b-1f68-4526-8d8e-e4e4fb4af186'
url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
# querystring = {"key": "a0a6d079-9f43-4dbc-b5e5-11e57a0dafb7"} 测试
querystring = {"key": "2124a91b-1f68-4526-8d8e-e4e4fb4af186"}
headers = {'Content-Type': "application/json"}

def send_images(image):
    with open(image, 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding='utf-8')
        my_md5 = hashlib.md5()
        img_data = base64.b64decode(image_base64)
        my_md5.update(img_data)
        myhash = my_md5.hexdigest()

    data = {
        "msgtype": "image",
        "image": {
            "base64": image_base64,
            "md5": myhash
        }
    }
    r = requests.post(url_i,json=data)
    status = json.loads(r.text)
    if status['errcode'] == 0:
        logger.info("图片发送成功")
    else:
        logger.error(status['errmsg'])

def send_md(body, msgtype):
    body = body.encode("utf-8").decode("latin1")
    msg = {"msgtype": msgtype}
    content = {"content": body}
    text = {msgtype: content}
    msg.update(text)
    response = requests.request("POST", url, data=json.dumps(msg, ensure_ascii=False), headers=headers,
                                params=querystring)
    return response.text

if __name__ == '__main__':
    send_images('results/pass_daily/2020-10-26.png')
