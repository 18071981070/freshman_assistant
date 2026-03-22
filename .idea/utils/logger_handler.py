import logging
from path_tool import get_abs_path
import os
from datetime import datetime 
# 日志保存的根目录
LOG_ROOT = get_abs_path('logs')  # 或者指定具体路径，例如：os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(LOG_ROOT, exist_ok=True)
#日志的格式配置
DEFAULT_LOG_FORMAT=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
def get_logger(name:str, log_file:str=None, level=logging.INFO,file_level:int=logging.DEBUG)->logging.Logger:
    logger=logging.getLogger(name)
    logger.setLevel(level)
    #避免重复添加handler
    if logger.hasHandlers():
        return logger
    #控制台handler
    console_handler=logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)
    #文件handler
    if not log_file:#日志文件的存放路径
        log_file=os.path.join(LOG_ROOT, f'{name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    file_handler=logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)
    return logger
#快捷获取日志器
logger=get_logger('app')
if __name__ == '__main__':
    logger.debug('这是一个调试日志')
    logger.info('这是一个信息日志')
    logger.warning('这是一个警告日志')
    logger.error('这是一个错误日志')
    logger.critical('这是一个严重错误日志')








