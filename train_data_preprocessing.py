#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import settings
import os
import shutil
from PIL import Image
from acquire_picture import save_image_to_file,img_denoise,img_split

# 从目标页面获取大量的验证码样本，进行预处理，处理后的验证码存储在change_picture文件夹中
def preprocessing():

    for i in range(150):
        save_image_to_file()
    dir = os.listdir(settings.raw_data_dir)
    for d in dir:
        img = Image.open(settings.raw_data_dir + d)
        img = img_denoise(img, 135)
        img.save(settings.change_data_dir + d)

# change_picture文件夹中的数据进行标注后，将验证码切分，切分后生成训练数据
def make_train_data():

    dir = os.listdir(settings.change_data_dir)
    for d in dir:
        img = Image.open(settings.change_data_dir + d)
        img_list = img_split(img,settings.img_split_start,settings.img_split_width)
        for i in range(4):
            label_dir = os.listdir(settings.train_data_dir)
            if d[i] in label_dir:
                img_list[i].save(settings.train_data_dir + d[i] + "/" + d)
            else:
                path = settings.train_data_dir + d[i]
                os.mkdir(path)
                img_list[i].save(path + "/" + d)

# 递归删除目录
def clean_dir(dir_name):

    shutil.rmtree(dir_name)
    os.mkdir(dir_name)

# clean_dir(settings.train_data_dir)
# clean_dir(settings.change_data_dir)
# clean_dir(settings.raw_data_dir)

if __name__ == "__main__":
    preprocessing()
    make_train_data()