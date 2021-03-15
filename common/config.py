# Developed Date; 2021-03-10
# Developer: Poon Ying Wai
# Description: 設定情報を管理するモジュール
#

import json
import enum
from common.singleton import Singleton

class AreaConfigKey(enum.Enum):
    """設定キーの値を保存する列挙型

　　　　以下のパラメータを定義しています。
　　　　CSV_URL：CSVファイルソースのURL（提供されている都道府県）

    """

    CSV_URL = "csv_url"
    ENCODING = "encoding"
    DATE_KEY = "date_key"
    DATE_FORMAT = "date_format"


class NoSuchAreaError(Exception):
    """設定されている地域以外の地域が選択されたときのエラー"""
    pass

class ConfigMan(metaclass=Singleton):
    """設定情報を管理するマネージャ
    """
    def __init__(self, conf_filepath: str):
        """コンストラクタ

        Args:
            conf_filepath: 設定ファイルのパス
        """
        with open(conf_filepath, "r") as conf_file:
            self._conf = json.load(conf_file)


    def get_conf(self, area): #県or市
        """設定情報を取得

        指定した都道府県の設定情報を取得する

        Args:
            area: 都道府県
        
        Returns:
            地域の設定情報

        Raises:
            NoSuchAreaError: 指定した地域が設定されない時のエラー
        """
        if not self._conf.get(area):
            raise NoSuchAreaError(f'指定した地域の設定ファイルが存在しません。area={area}')
        return self._conf[area]


if __name__ == "__main__":

    confman = ConfigMan('../config/config.json')
    print(confman.get_conf('kanagawa'))
    print(confman.get_conf('yokohama'))
