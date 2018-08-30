#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import os
import numpy as np
import pickle
import settings
from PIL import Image
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
from sklearn import svm
from sklearn.cross_validation import train_test_split
from recognition_code import img_verify_code
# 将图片转化为矩阵形式
def img_to_array(dir_name):

    x_data = []
    y_data = []
    name_list = os.listdir(dir_name)
    for name in name_list:
        if not os.path.isdir(os.path.join(dir_name, name)):
            continue
        image_files = os.listdir(os.path.join(dir_name, name))
        for img in image_files:
            i = Image.open(os.path.join(dir_name, name, img))
            x_data.append(np.array(i).flatten())
            y_data.append(name)
    return x_data,y_data

# 训练KNN模型
def knn_model(x_data,y_data):

    knn = KNeighborsClassifier()
    score = cross_val_score(knn,x_data,y_data,scoring='accuracy')
    average_accuracy = np.mean(score)*100
    print("准确率为：{0:.1f}%".format(average_accuracy))
    pickle.dump(knn, open("model.pkl", "wb+"))

# 训练SVM模型
def svm_model(x_data,y_data):

    SVM = svm.SVC()
    x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,random_state=14)
    SVM.fit(x_train,y_train)
    y_predict = SVM.predict(x_test)
    average_accuracy = np.mean(y_test==y_predict)*100
    print("准确率为：{0:.1f}%".format(average_accuracy))
    pickle.dump(SVM, open("model.pkl", "wb+"))


if __name__ == "__main__":
    x_data,y_data = img_to_array(settings.train_data_dir)
    #knn_model(x_data,y_data)
    svm_model(x_data,y_data)
