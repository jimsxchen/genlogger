import logging
from logging.handlers import *
import os
import queue

def set_logger(file_name:str, handler:str="rotatingfile", level:str="info", max_size=1024*1024*100, rotate_num=1, 
                host="localhost", port="51000", 
                mailhost=None, fromaddr=None, toaddrs=None, subject=None, 
                url=None, 
                queue:queue=None):

    # sanity check
    if (file_name == None or file_name == "") and (handler == "rotatingfile" or handler == "timedrotatingfile" or handler == "watchedfile"):
        raise ValueError("Must specify a valid log file name! For e.g. /data/lec.log")

    # if file_name includes a path. Check the folder existence. If not create.
    if (handler == "rotatingfile" or handler == "timedrotatingfile" or handler == "watchedfile"):
        if len(file_name.split("/")) > 1 and not os.path.exists("/".join(file_name.split("/")[:-1])):
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    # configure the root logger
    root_logger = logging.getLogger()
    log_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(log_level) 

    # sort out the handler
    if handler.lower() == "rotatingfile": 
        file_handler = RotatingFileHandler(file_name, maxBytes=max_size, backupCount=rotate_num)
    elif handler.lower() == "timedrotatingfile":
        file_handler = TimedRotatingFileHandler(file_name, backupCount=rotate_num)
    elif handler.lower() == "watchedfile":
        file_handler = WatchedFileHandler(file_name)
    elif handler.lower() == "socket":
        file_handler = SocketHandler(host, port)
    elif handler.lower() == "datagram":
        file_handler = DatagramHandler(host, port)
    elif handler.lower() == "syslog":
        file_handler = SysLogHandler()
    elif handler.lower() == "smtp" and mailhost != None and fromaddr != None and toaddrs != None and subject != None:
        file_handler = SMTPHandler(mailhost, fromaddr, toaddrs, subject)
    elif handler.lower() == "http" and url != None:
        file_handler = HTTPHandler(host, url)
    elif handler.lower() == "buffering":
        file_handler = BufferingHandler(max_size)
    elif handler.lower() == "memory":
        file_handler = MemoryHandler(max_size)
    elif handler.lower() == "queue" and queue != None:
        file_handler = QueueHandler(queue)
    else:
        file_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s — %(name)s — %(funcName)s:%(lineno)d — %(levelname)s — %(message)s")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
            

if __name__ == '__main__':
    print("start logging...")

    # *****************testing code**************
    set_logger("data/test_rotate.log", max_size=2048)
    set_logger("data/test_rotate.log", level="debug")
    logger = logging.getLogger(__name__)
    for i in range(1000):
        logger.info(f"Test log rotation {i}")
    # *****************testing code**************

    print("finished logging")



