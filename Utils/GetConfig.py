#encoding=utf-8
import configparser

class Config(object):

    def __init__(self,config_file_path):
        self.config_file_path = config_file_path
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file_path)

    #获取所有的section
    def get_all_sections(self):
        return self.config.sections()

    #获取option的值
    def get_option_value(self,section_name,option_name):
        value = self.config.get(section_name,option_name)
        return value

    #获取所有的section键值对
    def get_all_section_items(self,section_name):
        items = self.config.items(section_name)
        return  dict(items)

if __name__ == '__main__':
    from Config.ProjectVar import *
    print(interface_server_info_path)
    config = Config(interface_server_info_path)
    print(config.get_all_sections())
    print(config.get_all_section_items("interface_server"))
    ip = config.get_option_value("interface_server","ip")
    port = config.get_option_value("interface_server","port")
    print(ip,port)


