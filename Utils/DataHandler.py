#encoding:utf-8
# @Time : 2019/7/16 19:45 
# @Author : huhongqiang
# @File : DataHandler.py
import  hashlib,re
from Utils.GetUniqueNum import get_unique_number,global_vars
from Utils.Log import *
from Utils.HttpClient import http_request
import requests
from Utils.ParseExcel import ParseExcel
from Config.ProjectVar import *

def md5(s):
    md5 = hashlib.md5()
    md5.update(s.encode("utf-8"))
    md5_value = md5.hexdigest()
    return md5_value

#将请求数据中的${变量}的变量替换为唯一数或全局变量中的数值
def data_handler(data):
    if re.search(r"\$\{unique_num\d+\}",data):
        #匹配${unique_num1}形式的变量,获取变量名
        var_name = re.search(r"\$\{(unique_num\d+)\}",data).group(1)
        #获取文件中存储的变量对应的值
        var_value = get_unique_number(var_name)
        #把整个${}形式的数据替换成对应的值
        data = re.sub(r"\$\{unique_num\d+\}",str(var_value),data)
        #获取num1等字符串
        var_name = var_name.split("_")[1]
        #num1等对应的值存入全局变量，方便其他接口使用
        global_vars[var_name] = var_value
    #匹配并替换密码字段
    if re.search(r"\$\{md5\(\w+\)\}",data):
        str_value = re.search(r"\$\{md5\((\w+)\)\}",data).group(1)
        md5_value = md5(str_value)
        print("替换前 data",data)
        data = re.sub(r"\$\{md5\(\w+\)\}",md5_value,data)
        print("替换后 data", data)
        global_vars["md5"] = md5_value
    #将请求数据中变量的值替换为全局变量中对应的值
    if re.search(r"\$\{(\w+)\}",data):
        for var_name in re.findall(r"\$\{(\w+)\}",data):
            print("替换前 data", data)
            data = re.sub(r"\$\{%s\}" %var_name,str(global_vars[var_name]),data)
            print("替换后 data", data)
    return data


def send_request(interface_name,data,regx=None):
    #处理传入的请求数据
    data = data_handler(data)
    try:
        response = http_request(interface_name[1],interface_name[0],eval(data))
        return  response,data
    except Exception as e:
        print("调用接口出错 %s:%s" %(interface_name,data))
        print(e)
        return None,data

#获取接口响应数据中的关联关联变量值，存入全局变量中
def set_var_from_response(response,var_name,regx=None):
    if regx is None:
        return False

    if not isinstance(response,requests.models.Response):
        info('传入的响应结果对象类型不对,传入的响应:%s,响应类型%s' %(response,type(response)))
        return False
    try:
        if re.search(regx,response.text):
            var_value = re.search(regx,response.text).group(1)
            global_vars[var_name] = var_value
            return True
    except Exception as e:
        info("从响应结果提取变量值失败 响应:%s,变量:%s,正则表达式:%s" %(response,var_name,regx))
        return False


#获取需要执行的测试用例序号和测试用例sheet名，作为元组存入列表
def get_test_case_sheet_names(test_data_excel_path):
    #定义ParseExcel对象
    parseExcel = ParseExcel(test_data_excel_path)
    #设置当前sheet为第一个sheet
    parseExcel.set_sheet_by_index(0)
    #存放需要运行的测试用例序号，和测试用例sheet名
    test_case_to_run_sheet_names = []
    #遍历测试用例集的每行组成的列表
    for row in parseExcel.get_all_rows_values():
        #如果测试用例sheet名不为空且此行需要执行的话
        if row[test_case_test_step_sheet_name_col_no]  and \
                row[test_case_is_executed_col_no].lower() == "y":
            #测试用例集序号和测试用例sheet名组成的元组
            test_sheet_name_tuple = row[test_case_row_no_clo_no],row[test_case_test_step_sheet_name_col_no]
            #元组加入列表
            test_case_to_run_sheet_names.append(test_sheet_name_tuple)
    return test_case_to_run_sheet_names


#获取每条测试用例的数据
def test_cases_from_test_data_sheet(test_data_excel_path,test_data_sheet_name):
    parseExcel = ParseExcel(test_data_excel_path)
    #根据sheet名设置当前sheet
    parseExcel.set_sheet_by_name(test_data_sheet_name)
    info("当前的测试用例sheet名:%s" %test_data_sheet_name)
    #存放所有的接口测试用例
    test_cases = []
    #获取所有的测试用例
    #遍历每行数据
    for row in parseExcel.get_all_rows_values():
        #如果需要执行
        if  row[test_data_is_executed_col_no] and row[test_data_is_executed_col_no].lower() == "y":
            #获取测试用例序号,测试用例接口名，请求数据，断言数据，正则匹配表达式
            test_case = row[test_data_row_no_col_no],row[test_data_interface_name_col_no],row[test_data_request_data_col_no],\
                             row[test_data_assert_word_col_no],row[test_data_correlate_regx_col_no]
            #加入列表
            test_cases.append(test_case)
    return test_cases

if __name__ == "__main__":
    # print(md5("hhq123456"))
    # from Config.ProjectVar import test_data_file
    # datas = ['{"username":"testman${unique_num1}", "password":"123456789abc","email":"sed@qq.com"}','{"username": "testman${num1}", "password": "${md5(123456789abc)}"']#,'{"userid":${userid}, "token": "${token}", "title":"python", "content":"python port test"}']
    # for data in datas:
    #     print(data_handler(data))
    from Config.Interface import *
    #注册
    data = '{"username":"hhq${unique_num1}","password":"hhq123456","email":"sed@qq.com"}'
    res_tuple = send_request(register,data)
    response = res_tuple[0]
    print(response.text)
    #获取关联的userid
    print(set_var_from_response(response,"userid",'"userid": (\d+)'))
    print(global_vars)

    #获取测试用例sheet名
    from Config.ProjectVar import test_data_file
    print(get_test_case_sheet_names(test_data_file))

    #获取测试用例数据
    test_cases = test_cases_from_test_data_sheet(test_data_file,"博客api测试")
    print(test_cases)



