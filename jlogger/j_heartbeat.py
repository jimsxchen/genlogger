import time
import logging

class HeartbeatLog:
    """ heartbeat log class
    """
    def __init__(self, name, interval_env):
        self._name = name
        if interval_env is not None and interval_env.isdigit():     # Note, interval_env must be positive integer number!
            self._interval_val = int(interval_env)
        else:
            self._interval_val = 1
        self._start_time = None

    def log(self, logger:logging.Logger = None):
        if self._start_time == None:
            self._start_time = time.time()

        curr_time = time.time()
        if round(int(curr_time-self._start_time)) >= self._interval_val and logger != None:
            ori_fmtter = logger.root.handlers[0].formatter
            new_fmtter = logging.Formatter("%(asctime)s — " + self._name + " — %(funcName)s:%(lineno)d — %(levelname)s — %(message)s")
            logger.root.handlers[0].setFormatter(new_fmtter)
            logger.info(f'Heart beat ----- alive. Logged every {self._interval_val} seconds.')
            logger.root.handlers[0].setFormatter(ori_fmtter)               
            self._start_time = curr_time

