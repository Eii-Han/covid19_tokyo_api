from common.singleton import Singleton
import logging
import logging.config
import logging.handlers
import yaml


class SyslogMan(metaclass=Singleton):

    def __init__(self, filepath: str):
        logging.config.dictConfig(yaml.safe_load(open(filepath).read()))
        self._logger = logging.getLogger('syslogger')

    def log(self, message, level='debug'):
        if level == 'debug':
            self._logger.debug(message)
        elif level == 'info':
            self._logger.info(message)
        elif level == 'warning':
            self._logger.warning(message)
        elif level == 'error':
            self._logger.error(message)
        elif level == 'critical':
            self._logger.critical(message)
        else:
            pass

if __name__ == '__main__':
    sm = SyslogMan(filepath="../config/logger.yaml")
    sm.log('debug message')
    sm.log('info message', 'info')
    sm.log('warn message', 'warning')
    sm.log('error message', 'error')
    sm.log('critical message', 'critical')
