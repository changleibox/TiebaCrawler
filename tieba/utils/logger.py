#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by box on 2018/3/14.
import logging


class ColorFormatter(logging.Formatter):
    COLORS = {
        'HEADER': '\033[30m',
        logging.INFO: '\033[96m',
        logging.DEBUG: '\033[36m',
        logging.WARNING: '\033[92m',
        logging.ERROR: '\033[31m',
        logging.CRITICAL: '\033[33m',
        logging.NOTSET: '\033[0m',
        'ENDC': '\033[0m',
    }

    def format(self, record):
        return self.COLORS[record.levelno] + super(ColorFormatter, self).format(record) + self.COLORS['ENDC']


class Logger(object):

    def __init__(self, name=None):
        super(Logger, self).__init__()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.parent = None

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(ColorFormatter('%(levelname)s %(message)s'))
        self.logger.addHandler(ch)

    def debug(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        """
        self.logger.exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        self.logger.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
        """
        self.logger.log(msg, level, *args, **kwargs)


if __name__ == '__main__':
    for i in range(100):
        color = '033[%dm' % i
        print '\033[%dm' % i, color, '颜色', color, '\033[0m'
