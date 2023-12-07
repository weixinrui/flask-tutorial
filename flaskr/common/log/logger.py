import os
import threading
import logging
from logging import FileHandler, StreamHandler

def get_filepath(filename):
    
    log_path = os.path.join(os.path.split(os.path.realpath(__file__))[0],'../../logs')

    if not os.path.exists(log_path):
        os.mkdir(log_path)
    
    if filename is None:
        filepath = os.path.join(log_path,"flaskr.log")
    else:
        filepath = os.path.join(log_path,filename)
    return filepath

class RunLogger:
    __instance_lock = threading.Lock()

    def __init__(self,level,formatter,filename=None):
        self.level = level
        self.log_formatter = formatter
        self.filename = filename
        self.filepath = get_filepath(filename)
        self.logger = self.__get_logger()

    def __new__(cls,*args,**kwargs):
        if not hasattr(RunLogger,'_instance'):
            with RunLogger.__instance_lock:
                if not hasattr(RunLogger,'_instance'):
                    RunLogger._instance = object.__new__(cls)
        return RunLogger._instance
    
    def get_file_handle(self):
        handle = FileHandler(self.filepath,encoding='utf-8')
        handle.setFormatter(self.log_formatter)
        return handle

    def get_stream_handle(self):
        handle = StreamHandler(filename=self.filepath,encoding='utf-8')
        handle.setFormatter(self.log_formatter)
        return handle
    
    def __get_logger(self):
        if self.filename is None:
            logger = logging.getLogger("run.log")
        else:
            logger = logging.getLogger(self.filename)
        logger.setLevel(self.level)
        return logger
    