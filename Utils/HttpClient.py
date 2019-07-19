# encoding:utf-8
# @Time : 2019/7/12 21:40 
import requests
import json
from Utils.Log import *

def http_request(url,request_method,request_content):
    if request_method == "get":
        try:
            if isinstance(request_content,dict):
                info("请求的接口地址是:%s"%url)
                info("请求的数据是:%" %request_content)
                #请求参数是字典
                res = requests.get(url,params=request_content)
            else:
                info("请求的接口地址是:%s" % url)
                info("请求的数据是:%s" % request_content)
                res = requests.get(url+str(request_content))
        except Exception as e:
            info("get请求发生异常,请求url %s ，请求内容:%s ,请求异常%s" %(url,request_content,e))
            raise e
        return res
    elif request_method == "post":
        try:
            if isinstance(request_content,dict):
                info("请求方式是:%s" %request_method)
                info("请求的接口地址是:%s" %url)
                info("请求的数据是:%s" %request_content)
                res = requests.post(url,data=json.dumps(request_content))
            else:
                raise ValueError
        except Exception as e:
            info("post请求发生异常,请求url %s ，请求内容:%s ,请求异常%s" % (url, request_content, e))
            raise e
        return res
    elif request_method == "put":
        try:
            if isinstance(request_content,dict):
                info("请求的接口地址是:%s" %url)
                info("请求的数据是:%s" % request_content)
                info("请求方式是:%s" %request_method)
                res = requests.put(url,data=json.dumps(request_content))
        except Exception as e:
            info("put请求发生异常,请求url %s ，请求内容:%s ,请求异常%s" % (url, request_content, e))
            raise e
        return res

if __name__ == "__main__":
    from Utils.GetUniqueNum import get_unique_number
    import re
    #注册
    num = get_unique_number("unique_num1")
    username = "hhq" + str(num)
    url_1 = "http://39.106.41.11:8080/register/"
    data = {"username":username,"password":"hhq123456","email":"sed@qq.com"}
    res = http_request(url_1,"post",data)
    print(res.status_code)
    print(res.text)
    #提取userid
    userid = re.search(r"userid\": (\d+)",res.text).group(1)
    # print(userid)
    userid = int(userid)


    #登录
    import hashlib
    md5 = hashlib.md5()
    md5.update('hhq123456'.encode("utf-8"))
    pwd = md5.hexdigest()
    url_2 = "http://39.106.41.11:8080/login/"
    data = {"username":username, "password": pwd}
    res = http_request(url_2,"post",data)
    print(res.status_code)
    print(res.text)
    #获取token
    token = re.search(r'token\": "(\w+)"',res.text).group(1)
    print("token",token)

    #创建博客
    url = "http://39.106.41.11:8080/create/"
    data =  {'userid': userid, 'token': token, 'title': "mysql ",'content': 'mysql learn'}
    res = http_request(url,"post",data)
    print(res.text)


    #查询用户的博文
    url ="http://39.106.41.11:8080/getBlogsOfUser/"
    data = {"userid":userid, "token": token}
    res = http_request(url, "post",request_content=data)
    print(res.text)
    #提取博文id
    articleId = re.search(r'"articleId": (\d+)',res.text).group(1)
    print("articleId",articleId)

    #获取博文
    url = "http://39.106.41.11:8080/getBlogContent/"
    res = http_request(url,"get",articleId)
    print(res.text)



