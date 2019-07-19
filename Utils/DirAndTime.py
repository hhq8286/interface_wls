#encoding=utf-8
import time,os
#导入locale模块，设置支持中文
import  locale
locale.setlocale(locale.LC_CTYPE,"chinese")

#获取当前日期
def get_current_date():
    current_date = time.strftime("%Y年%m月%d日")
    return  current_date

#获取当前时间
def get_current_time():
    current_time = time.strftime("%H时%M分%S秒")
    return  current_time


#创建以日期命名的目录
def create_date_dir(dir_path):
    if os.path.exists(dir_path):
        current_date = get_current_date()
        path = os.path.join(dir_path,current_date)
        if not os.path.exists(path):
            os.mkdir(path)
        return current_date
    else:
        raise Exception("dir path does not exist!")


#创建以时间命名的目录
def create_time_dir(dir_path):
    if os.path.exists(dir_path):
        current_time = get_current_time()
        path = os.path.join(dir_path,current_time)
        if not os.path.exists(path):
            os.mkdir(path)
            return current_time
    else:
        raise Exception("dir path does not exist!")

if __name__ == "__main__":
    print(get_current_date())
    print(get_current_time())
    print(create_date_dir("d:\\"))
    print(create_time_dir("d:\\"))


