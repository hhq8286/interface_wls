#encoding=utf-8
from Config.Interface import *
from Config.ProjectVar import *
from Utils.ParseExcel import ParseExcel
from Utils.DataHandler import *
import time
from Utils.SendMailWithAtt import Mail

def main():
    #定义ParseExcel对象
    parseExcel = ParseExcel(test_data_file)
    #
    test_results_for_html_report  = []
    #获取测试用例集中的所有测试用例sheet名
    test_sheet_names = get_test_case_sheet_names(test_data_file)
    # print(test_sheet_names
    #遍历每个测试用例sheet，test_sheet_name为一个元组，包含序号和sheet名
    for test_sheet_name  in test_sheet_names:
        print("*"*20)
        #测试用例集对应的测试执行结果
        flag = True
        #设置当前sheet
        parseExcel.set_sheet_by_name(test_sheet_name[1])
        #获取测试用例sheet的所有测试用例,test_sheet_name是元组（用例编号，sheet名）
        test_cases = test_cases_from_test_data_sheet(test_data_file,test_sheet_name[1])
        #遍历每个测试用例
        for test_case in test_cases:
            print("----" * 20)
            #获取接口名和请求数据
            interface_name = eval(test_case[1])
            request_data = test_case[2]
            # print(interface_name,request_data)
            start_time = time.time()
            #发送接口请求
            res,data = send_request(interface_name,request_data)
            end_time = time.time()
            info("接口响应信息:%s" %res.text)
            #写响应信息到文件,行列都是从1开始
            parseExcel.write_cell_value(int(test_case[0])+1,test_data_response_data_col_no+1,res.text)
            info("断言值: %s" %test_case[3])
            #写测试用例执行时间
            parseExcel.write_current_time(int(test_case[0])+1,test_data_executed_time_col_no+1)
            try:
                #利用正则表达式断言接口是否成功
                assert_word = test_case[3]
                #断言失败，抛断言异常
                if not re.search(assert_word,res.text):
                    raise AssertionError
                #写成功的测试结果
                print("hhhhhhh",test_case[0])
                parseExcel.write_cell_value(int(test_case[0])+1,test_data_test_result_col_no + 1,"成功",style="green")
                #
                test_results_for_html_report.append((res.url,data,res.text,int(end_time-start_time)*1000,test_case[3],"成功"))
            except AssertionError as e:
                #写失败的测试结果
                parseExcel.write_cell_value(int(test_case[0])+1,test_data_test_result_col_no + 1,"失败",style="red")
                test_results_for_html_report.append((res.url, data, res.text, int(end_time - start_time) * 1000, test_case[3], "失败"))
                flag = False
            except Exception as e:
                #写失败的测试结果
                parseExcel.write_cell_value(int(test_case[0])+1,test_data_test_result_col_no + 1,"失败",style="red")
                test_results_for_html_report.append((res.url,data,res.text,int(end_time - start_time) * 1000, test_case[3], "失败"))
                flag = False
            info("接口执行耗时:[%s] 毫秒" %(end_time - start_time))
            #写入接口执行耗时
            parseExcel.write_cell_value(int(test_case[0])+1,test_data_test_elapse_time_col_no + 1,str(int(end_time - start_time) * 1000))
            #处理关联数据，并存储关联数据到全局变量
            #获取关联正则表达式
            regx = test_case[4]
            if regx:
                var_name = regx.split('||')[0]
                regx_info = regx.split("||")[1]
                #提取的关联数据不为空的话
                if re.search(regx_info,res.text).group(1):
                    #提取响应中的关联数据
                    var_value = re.search(regx_info,res.text).group(1)
                    #存入全局变量的值
                    global_vars[var_name] = var_value
                    info("提取的响应变量:%s,变量值:%s" %(var_name,var_value))
                    info("全局变量: %s" %global_vars)
        #切换到测试用例集sheet
        parseExcel.set_sheet_by_index(0)
        if flag:
            #写测试用例集测试执行结果
            parseExcel.write_cell_value(int(test_sheet_name[0]) + 1,
                                        test_case_executed_result_col_no,"成功",style="green")
        else:
            parseExcel.write_cell_value(int(test_sheet_name[0]) + 1,
                                        test_case_executed_result_col_no, "失败", style="red")
        #写测试用例集测试执行时间
        parseExcel.write_current_time(int(test_sheet_name[0]) + 1,test_case_executed_time_col_no)
    mail = Mail(mail_host,mail_user,mail_pass,sender)
    #发送邮件
    mail.send_mail(receivers,"接口测试报告","接口测试报告",test_data_file)

if __name__ == "__main__":
    main()