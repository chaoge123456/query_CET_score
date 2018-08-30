#!/usr/bin/env python
#_*_ coding:utf-8 _*_

threshold=135  # 二值化阙值
img_split_start = 20  # 切割验证码起点
img_split_width = 35  # 切割验证码宽度
raw_data_dir = "images/raw_picture/"  # 原始验证码文件夹
change_data_dir = "images/change_picture/"  # 处理后的验证码文件夹
train_data_dir = "images/train_data/"  # 训练数据文件夹
PROXY_POOL_URL = 'http://localhost:5555/random' # 本地获取代理连接

# 获取验证码的请求头
img_api_headers = {
    "Host": "cache.neea.edu.cn",
    "Proxy-Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
    "Accept": "*/*",
    "DNT": "1",
    "Referer": "http://cet.neea.edu.cn/cet/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Cookie": "UM_distinctid=15ddab8ea07302-04182c5cab6868-791238-1fa400-"
              "15ddab8ea0976; BIGipServercache.neea.edu.cn_pool=2577451018"
              ".39455.0000; verify=enc|ba3633d8066b323cd1e4139c90a0f5ea84c"
              "a7e0112463eecd718e0949306c91f; Hm_lvt_dc1d69ab90346d48ee02f"
              "18510292577=1503370065,1503371098,1503372217,1503372362; Hm_"
              "lpvt_dc1d69ab90346d48ee02f18510292577=1503372362"
}

# 查询操作的请求头
query_api_headers = {
    "Host": "cache.neea.edu.cn",
    "Proxy-Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Origin": "http://cet.neea.edu.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "DNT": "1",
    "Referer": "http://cet.neea.edu.cn/cet/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Cookie": "UM_distinctid=15ddab8ea07302-04182c5cab6868-791238-1fa400-"
              "15ddab8ea0976; BIGipServercache.neea.edu.cn_pool=2577451018"
              ".39455.0000; verify=enc|ba3633d8066b323cd1e4139c90a0f5ea84c"
              "a7e0112463eecd718e0949306c91f; Hm_lvt_dc1d69ab90346d48ee02f"
              "18510292577=1503370065,1503371098,1503372217,1503372362; Hm_"
              "lpvt_dc1d69ab90346d48ee02f18510292577=1503372362"
}

# 请求验证码页面URL
image_api = "http://cache.neea.edu.cn/Imgs.do?c=CET&ik={id}&t=0.6002525141319914"
# 查询操作URL
query_api = "http://cache.neea.edu.cn/cet/query"
