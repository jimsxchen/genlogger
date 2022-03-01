import logging
from jlogger import j_logger
import unittest


class TestRotatingFileLog(unittest.TestCase):
    def setUp(self):
        j_logger.set_logger("rotate_logger_unittest.log", max_size=2048)
        self.logger=logging.getLogger(__name__)

    def test_wrap_test(self):
        assert self.logger.hasHandlers()
        for i in range(200):
            self.logger.info(f"Testing wrap and rotate. {i} ")



if __name__ == '__main__':
    unittest.main()
