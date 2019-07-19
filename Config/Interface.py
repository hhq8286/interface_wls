# encoding:utf-8
# @Time : 2019/7/13 13:31 
# @Author : huhongqiang
# @File : Interface.py
from Config.ProjectVar import *
import os
from Utils.GetConfig import Config
#
interface_config_file = os.path.join(project_path,"Config","interface_server_info.ini")
#定义Config对象
config = Config(interface_config_file)
#获取配置文件中的ip和port
ip = config.get_option_value("interface_server","ip")
port = config.get_option_value("interface_server","port")

#把请求方法和url存入元组中
register = ("post","http://%s:%s/register/" %(ip,port))
login =  ("post","http://%s:%s/login/" %(ip,port))
create =("post","http://%s:%s/create/" %(ip,port))
getblogsofuser = ("post","http://%s:%s/getBlogsOfUser/" %(ip,port))
getblogcontent = ("get","http://%s:%s/getBlogContent/" %(ip,port))
update = ("put","http://%s:%s/update/" %(ip,port))
delete = ("post","http://%s:%s/delete/" %(ip,port))

if __name__ == '__main__':
    print(ip)
    print(port)
    print(register)
    print(login)
    print(create)