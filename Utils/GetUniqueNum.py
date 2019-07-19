# encoding:utf-8
# @Time : 2019/7/12 22:13 
# @Author : huhongqiang
# @File : GetUniqueNum.py
import pickle
import os
from Config.ProjectVar import project_path
from Utils.Log import *
#存放全局唯一数值
global_vars = {}
def get_unique_number(unique_number):
    global global_vars
    #文件存放路径
    data_file = os.path.join(project_path,"Config","StaticVarDataFile")
    try:
        with open(data_file,"rb") as fp:
            #读取存储的文件，返回字典
            var = pickle.load(fp)
            #获取unique_number对应的value值
            data = var[unique_number]
            info("全局唯一数当前值是:%s" %data)
            #unique_number和对应的值存入全局变量
            global_vars[unique_number] = str(data)
            #值增加1
            var[unique_number] += 1
        #值+1后的字典写入文件
        with open(data_file,"wb") as file_obj:
            pickle.dump(var,file_obj)
    except Exception as e:
        info("获取测试框架的全局唯一数变量值失败，请求的全局唯一数变量是%s,异常原因如下：%s" %(unique_number,e))
        data = None
    finally:
        return  data

#利用txt文件读取、存储唯一变量值
def get_unique_num(unique_number):
    global  global_vars
    #唯一值文件txt文件
    data_file = os.path.join(project_path,"TestData","uniquenumber.txt")
    try:
        with open(data_file,"r+") as file_obj:
            #读取字典内容字符串
            content_dict = file_obj.readline().strip()
            #字符串转换成字典
            content_dict = eval(content_dict)
            #取出参数unique_number对应的值
            data = content_dict[unique_number]
            #取出的值存入全局变量
            global_vars[unique_number] = data
            #值+1
            content_dict[unique_number] += 1
            #定位到文件开头
            file_obj.seek(0,0)
            #值加1后的字典转成字符串写回文件
            file_obj.write(str(content_dict))

    except Exception as e:
        info("获取全局变量%s 的值失败 ，异常: %s" %(unique_number,e))
    finally:
        return data
if __name__ == "__main__":
    # data_file = os.path.join(project_path, "Config", "StaticVarDataFile")
    # data = {"unique_num1": 100, "unique_num2": 1000}
    # with open(data_file,"wb") as fp:
    #     pickle.dump(data,fp)
    # with open(data_file,"rb") as file_obj:
    #     content = pickle.load(file_obj)
    # print(type(content))
    # print(content)
    # print(get_unique_number("unique_num1"))
    # print(get_unique_number("unique_num2"))
    # print(global_vars)
    print(get_unique_num("unique_num1"))
    print(get_unique_num("unique_num2"))
    print(global_vars)