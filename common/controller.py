# Developed Date; 2021-03-10
# Developer: Poon Ying Wai
# Description: DataFrameの生成やロガー設定などの初期の処理をコントロールするモジュール
#
import pandas as pd

from common.singleton import Singleton
from common.config import ConfigMan
from common.pandas_man import PandasHolder
from common.syslogsender import SyslogSender
import collections


class Controller(metaclass=Singleton):
    """初期の処理を制御するクラス

    Attributes:
        _conf_man: コンフィグマネージャ
        _sm:　シスログマネージャ
    """

    def __init__(self):
        """Controllerのコンストラクタ

        以下の初期化を行います
        ・コンフィグマネージャ
        ・シスログマネージャ
        """
        self._conf_man = ConfigMan('config/config.json')
        self._sm = SyslogSender('config/logger.yaml')

    def get_config_json(self, area: str) -> dict:
        """地域のコンフィグ取得メソッド

        areaを引き渡し、コンフィグマネージャから取得する。

        Args:
            area: 地域名

        Returns:
            地域のコンフィグ
        """
        return self._conf_man.get_conf(area)

    def get_syslog_man(self) -> SyslogSender:
        """シスログマネジャー取得メソッド

        シスログマネジャーのインスタンスを返す

        Returns:
            シスログマネジャー
        """
        return self._sm

    def get_dataframe(self, area: str, force: bool) -> pd.DataFrame:
        """データフレーム取得メソッド

        以下の処理を行います。
        ・定義ファイルクラスから指定した地域の設定を取得
        ・PandasHolderにキャッシュされたデータを更新
        　もともと存在しない場合、新規取得
        ・データフレームを取得してリターンする

        Args:
            area: データフレーム取得対象の地域
            force: 強制更新かどうか

        Returns:
            対象地域のデータフレーム
        """
        conf_json = self.get_config_json(area)
        pd_holder = PandasHolder()
        pd_holder.add_data(area, conf_json, force)
        df = pd_holder.get_data(area, "dated_df")
        return df

    def flatten(self, args):
        """二次元の配列を一次元に平坦化するメソッド

        対象配列をループで回し、平坦化可能のものなら、yield from文でこのメソッドを再帰呼び出して
        処理を委譲する。
        ※yield from iterableは for item in iterable: yield itemと同等らしいです

        平坦化不可能まで平坦化した場合、一般的なyield文でジェネレータに委譲する。

        Args:
            args:平坦化対象の多次元リスト

        Yields:
            最低次元（一次元）の文字列またはバイト型
        """
        for arg in args:
            if isinstance(arg, collections.abc.Iterable) and not isinstance(arg, (str, bytes)):
                yield from self.flatten(arg)
            else:
                yield arg
