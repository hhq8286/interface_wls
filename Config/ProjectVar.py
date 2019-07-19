#encoding=utf-8
import os
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_conf_path = os.path.join(project_path,"Config","Logger.conf")

interface_server_info_path = os.path.join(project_path,"Config","interface_server_info.ini")

test_data_file = os.path.join(project_path,"TestData","接口测试数据.xlsx")

mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "286542822@qq.com"  # 用户名
mail_pass = "dsssmsrpvbuecaac"  # 口令

sender = '286542822@qq.com'
receivers = ['286542822@qq.com',"hhq8286@163.com" ]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


test_case_sheet = "测试用例"
#测试用例集合对应的列名
test_case_row_no_clo_no = 0
test_case_test_step_sheet_name_col_no = 2
test_case_is_executed_col_no = 3
test_case_executed_result_col_no = 7
test_case_executed_time_col_no = 8

test_data_row_no_col_no = 0
test_data_interface_name_col_no = 1
test_data_request_data_col_no = 2
test_data_response_data_col_no = 3
test_data_assert_word_col_no = 4
test_data_test_result_col_no = 5
test_data_correlate_regx_col_no = 6
test_data_test_elapse_time_col_no = 7
test_data_is_executed_col_no = 8
test_data_executed_time_col_no = 9


if __name__ == '__main__':
    print(project_path)
    print(log_conf_path)
