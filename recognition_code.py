#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import pickle
import numpy as np
import sys
import requests
import settings
from PIL import Image
from acquire_picture import img_denoise,img_split,img_list_to_array_list,get_image_url_and_filename
from io import BytesIO
from settings import image_api, query_api, img_api_headers, query_api_headers

myid = "3400801812{id:05d}"
name = "张晓雪"
global proxy
proxy = {'http': 'http://127.0.0.1:1080','https': 'http://127.0.0.1:1080'}

# 识别验证码
def img_verify_code(img):

    img = img_denoise(img,settings.threshold)
    img_list = img_split(img,settings.img_split_start,settings.img_split_width)
    array_list = img_list_to_array_list(img_list)
    model = pickle.load(open("model.pkl", "rb+"))
    code = model.predict(array_list)
    return "".join(code)

# 获取代理
def get_proxy():
    while True:
        try:
            response = requests.get(settings.PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            continue

# 打印日志
def log_info(s,id):
    if s == "error":
        print("日志-->验证码正确，但用户信息不匹配，查询结果为空，继续测试下一项：",id)
    else:
        print("日志-->抱歉，验证码错误：",id)

# 查询操作
def send_query_until_true(num):
    # 生成准考证号
    global proxy
    new_id = myid.format(id=num)
    # 获取验证码图片地址
    img_api_url = image_api.format(id=new_id)
    while True:
        try:
            img_api_resp = requests.get(img_api_url, headers=img_api_headers,timeout=10,proxies=proxy)
            img_url, filename = get_image_url_and_filename(img_api_resp.text)
            # 获取验证码图片并猜测
            img_resp = requests.get(img_url, timeout=10, proxies=proxy)
            if img_resp.status_code == 200:
                images = Image.open(BytesIO(img_resp.content))
                code = img_verify_code(images)
            else:
                code = "xxxx"
        except Exception:
            print("重新获取代理")
            p = str(get_proxy())
            proxy = {'http': 'http://' + p, 'https': 'http://' + p}
        else:
            break

    # CET4成绩查询选项
    # data = {"data": "CET4_181_DANGCI,{id},{name}".format(id=new_id, name=name),"v": code}
    # CET6成绩查询选项
    data = {"data": "CET6_181_DANGCI,{id},{name}".format(id=new_id, name=name),"v": code}
    query_resp = requests.post(query_api, data=data, headers=query_api_headers)
    query_text = query_resp.text
    log_info(query_text.split("'")[3],new_id)
    if "验证码错误" in query_text:
        query_text = send_query_until_true(num)
    # elif "您查询的结果为空" in query_text:
    #     images.save("images/save_picture/" + code + ".png")
    return query_text

def main():

    m = int(sys.argv[1]) # 开始区间
    n = int(sys.argv[2]) # 结束区间
    for i in range(m,n):
        for j in range(0,31):
            num = i*100+j
            query_text = send_query_until_true(num)
            if "您查询的结果为空" in query_text:
                continue
            else:
                print("您的准考证后五位是(不足五位的在前面补0)：", num)
                return True

if __name__ == '__main__':
    main()