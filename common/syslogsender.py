# Developed Date; 2021-05-01
# Developer: Poon Ying Wai
# Description:　システムログの出力機能を提供するモジュール
#

from common.singleton import Singleton
import logging
import logging.config
import logging.handlers
import yaml


class NoLevelError(Exception):
    """存在しないログレベルを指定されたときのエラー"""
    pass


class SyslogSender(metaclass=Singleton):
    """システムログ出力クラス

    Attributes:
        _logger: シスロガー
    """
    def __init__(self, filepath: str):
        """SyslogSenderのコンストラクタ

        ログ定義ファイルのファイルパスを受け取って、YAML形式で読み込み、
        シスロガーを生成する

        Args:
            filepath:　シスロガー定義ファイルのパス
        """
        logging.config.dictConfig(yaml.safe_load(open(filepath).read()))
        self._logger = logging.getLogger('syslogger')

    def log(self, message, level='debug') -> None:
        """ログ出力メソッド

        指定されたレベルに応じてログを出力する
        以下のレベルで出力できる
        ・debug
        ・info
        ・warning
        ・error
        ・critical

        Args:
            message: メッセージ本文
            level: ログレベル
        Raises:
            NoLevelError:　存在しないログレベルを指定されたときのエラー
        """
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
            raise NoLevelError(f'無効なメッセージのレベルです。level={level}')


if __name__ == '__main__':
    sm = SyslogSender(filepath="../config/logger.yaml")
    sm.log('debug message')
    sm.log('info message', 'info')
    sm.log('warn message', 'warning')
    sm.log('error message', 'error')
    sm.log('critical message', 'critical')
