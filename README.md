Introduction
============
jlogger package has two modules: j_logger and j_heartbeat.

j_logger is a generic package for properly setting up the loggers for application (with app main and sub-modules) in a hierachy way to present better information as per the message source, file name, time and the code line in file.  

j_heartbeat provides a heartbeat logging for any forever loop, either process or thread.


Installation Instructions
=========================
From PyPi with pip:

```
pip install jlogger
pip install --upgrade jlogger
```
Installation from source code is straight forward:

```
python setup.py install
```

Detail Explanaton and Usage - j_logger
======================================
This module provides a single function (set_logger) to wrap up the nitty-gritty setups for named loggers within the application hierachy. The application can call this many times to set up different handlers as requested. Once set, it will direct the logging message to all handlers. The default handler is a rotating file handler which will rotate when the log file reaches the specified maximum size (default to 50MB) so would not fill up the disk. It also sets a pre-difined formatter in the root logger which the user can alter it if needed.

- Let's get hands on. Example:

Assuming an application package has the following structure:

```
my_app/
    __init__.py
    main_app.py
    submodules/
        __init__.py
        module1.py
        module2.py
    test/
        unittest.py
```

In the main_app.py 

```
import logging
from jlogger.j_logger import set_logger
logger = logging.getLogger(__name__)

......
if __name__ == '__main__':
    ......
    set_logger("main_app.log")     
    logger.info("*** Main app started ***")
    ......
```

In submodules module1.py and module2.py


```
import logging   
logger = logging.getLogger(__name__)
    ......
    logger.info(f"Raw data received.")
    ......
    logger.warning(f"Temperature too high.")
    ......
```


- Explanation

In the main_app, it sets up a root logger and logs all messages (including the submodules) to the "main_app.log" file. Different module will have its own name in the log message. The logged message format looks like below:
```
         date time        module name   func:line No. level   message
--------------------------------------------------------------------------------------------------------
2022-03-03 14:43:25,926 — main_app.py — main_loop:153 — INFO — Waiting for communication to be connected.
......
2022-03-03 14:43:26,014 — module1.py — start:130 — DEBUG — Opening serial connection successfully.
```

The default root logger level is set to "DEBUG", rotating file handler, maximum file size is 5MB, the default rotating file number (rotate_num) is 1. All these settings can be changed by passing the name/value pairs. See below prototype for more details. 

When the live log file reaches 5MB, it saves it to a backup file the same name as the live one but with suffix of ".1". When the live log reaches 5MB again it overwrites (replaces) the backup file so on so the log file size is capped to maximum 2*5MB.

If the user wants different logging level for submodules, can set this in the main_app after the set_logger call. Example:

```
    logging.getLogger('submodules.module1').setLevel("INFO")    # remember the default root log level is DEBUG!
```

The set_logger function can be called many times to set up different handlers as required. So the log can be saved to the file, and sent via an email or to the cloud for e.g.


- The prototype:

```
def set_logger(file_name:str, handler:str="rotatingfile", level:str="info", max_size=1024*1024*50, rotate_num=1, 
                host="localhost", port="51000", 
                mailhost=None, fromaddr=None, toaddrs=None, subject=None, 
                url=None, 
                queue:queue=None):
```

Where:
```
    :param file_name: the logger file name from the app 
    :param handler: the type of the handler. default to rotatingfile. It can also be:
                timedrotatingfile, watchedfile, socket, datagram
                syslog, smtp, http, buffering, memory, queue
                Note: each type has different argument set and has to be provided properly 
    :param level: The logging level for the root logger. Value needs to be in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
                If the specified is not in the list, INFO is the default
    :param max_size: This argument is for rotating logs to specify the maximum log size. In mega byte.
    :param rotate_num: For rotating logs only. It specifies how many backup file needed. The value has to be
                at least 1 to work with rotation
    :param host: For socket, datagram, http types of logger to specify the host name or IP address 
    :param port: For socket, datagram, http types of logger to specify the port number
    :param mailhost: For smtp type to set up the mail server
    :param fromaddr: For smtp type to set up the mail sender address
    :param toaddrs: For smtp type to set up the mail recipient address
    :param subject: For smtp type to set up the mail subject
    :param url: For http handler to specify the website url
    :param queue: For queue handler to pass a queue object
```



Detail Explanaton and Usage - j_heartbeat
=========================================
The module provides a class to allow the user to use it in any forever loop (main while true or even thread) to log a heartbeat message something like below to indicate the process/thread is alive:

2022-03-03 14:43:41,060 — main_app — log:24 — INFO — Heart beat ----- alive. Logged every 5 seconds.

It takes care of the time expiration check according to the specified interval. If interval is set to 0, nothing happens.


- Example:

```
import logging   
from jlogger.j_heartbeat import HeartbeatLog   
logger = logging.getLogger(__name__)

......

heartbeat = HeartbeatLog("my_module", "5")
while True:
    ......
    heartbeat.log(logger)
```

- The class prototype


```
class HeartbeatLog:
    def __init__(self, name, interval_env:str):
        """ constructor
        :param name: The forever module name passed from app
        :param interval_env: interval for the heartbeat log (must be a string). When it is set to 0, it won't log the heartbeat.
        """

    def log(self, logger:logging.Logger = None):
        """ log function
        :param logger: The underlying logger. If this is None, it won't log.
        Note, if interval value is 0, it won't log.
        """
```

