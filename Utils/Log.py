#encoding=utf-8
from Config.ProjectVar import *
import logging.config
import logging
log_conf_path = os.path.join(project_path,"Config","Logger.conf")
#导入配置文件
logging.config.fileConfig(log_conf_path)
logger = logging.getLogger("example01")


def debug(message):
    logger.debug(message)

def info(message):
    logger.info(message)

def warning(message):
    logger.warning(message)

def error(message):
    logger.error(message)

if __name__ == "__main__":
    debug("debug")
    info("info")
    error("error")
    warning("warning")
    print(log_conf_path)