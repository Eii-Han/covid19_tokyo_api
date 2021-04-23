# Developed Date; 2021-03-10
# Developer: Poon Ying Wai
# Description: pandasライブラリで定義したクラスを管理するモジュール
#

import pandas as pd
import datetime
import io
import enum
import typing

from common.singleton import Singleton
from flask.cli import _validate_key
from builtins import staticmethod

class InvalidKeyError(Exception):
    pass

class DataFrameMetaKey(enum.Enum):
    """DataFrameのメタ情報キーの値を保存する列挙型

　  以下のパラメータを定義しています。
    CREATED_DATE: 生成日時
    UPDATED_DATE: 更新日時
    DATAFRAME:　DataFrame本体

    """

    CREATED_DATE = "_createdDate"
    UPDATED_DATE = "_updatedDate"
    DATAFRAME = "dated_df"

class PandasHolder(metaclass=Singleton):
    """pandasの地域感染情報保存用のクラス
    
    Attributes:
        _data_src: 全データ格納用の変数
    """

    def __init__(self):
        """コンストラクタ
        
        全データ格納用の変数を初期化する（初回のみ）
        """
        self._data_src = dict()

    def add_data(self, data_name: str, data_obj: io.StringIO, rename_dict: dict, forced: bool = False):
        """新しい感染情報を追加するメソッド

        指定した地域の当日の最新感染情報をDataFrameに追加・更新するメソッド
        forcedが真の場合、当日のデータがあっても強制更新を実行する

        Args:
            data_name: 地域の感染情報データの識別名
            data_obj:感染情報データのファイルオブジェクト
            rename_dict: 各カラムの再命名するためのメタ情報
            forced: 強制更新かどうかを判定するための引数
        """
        
        # 現在時刻を取得
        dt_now = datetime.datetime.now()
        now_str = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        
        # 患者データをキャッシュに保存するデータフレームを生成
        if forced or now_str != self.get_data(data_name, DataFrameMetaKey.UPDATED_DATE):
            if not self._data_src.get(data_name):
                self._data_src[data_name] = dict()
                self._data_src[data_name][DataFrameMetaKey.CREATED_DATE] = now_str 
            self._data_src[data_name][DataFrameMetaKey.UPDATED_DATE] = now_str
            self._data_src[data_name][DataFrameMetaKey.DATAFRAME] = self._create_dataframe(data_obj, rename_dict)

    def get_data(self, data_name: str, meta_key: typing.Union[DataFrameMetaKey, str]) -> typing.Any:
        """特定のデータ取得メソッド
        
         キャッシュされたデータフレームから地域の感染情報を取得して、
        meta_keyで指定したデータを取得する
        
        Args:
            data_name: 地域の感染情報データの識別名
            meta_key: メタキー
        Returns:
            特定のデータ
        """
        if not self._data_src.get(data_name):
            return None
        meta_key = self._change_key(meta_key)
        return self._data_src[data_name].get(meta_key)

    @staticmethod
    def _change_key(meta_key: typing.Union[DataFrameMetaKey, str]) -> DataFrameMetaKey:
        """キーの値変更メソッド
        
        列挙型のDataFrameMetaKeyキー値を文字列型に変更する。
        
        Args:
            data_name: 地域の感染情報データの識別名
            meta_key: メタキー
        Returns:
            特定のデータ
        """
        if isinstance(meta_key, str):
            for m_key in DataFrameMetaKey:
                if m_key.value == meta_key:
                    meta_key = m_key
                    break
            else:
                raise InvalidKeyError("DataFrameMetaKeyクラスで定義したキーを使用してください")
        return meta_key

    @staticmethod
    def _create_dataframe(data_obj, rename_dict):
        df = pd.read_csv(data_obj, header=0)
        df.rename(columns=rename_dict, inplace=True)
        df = df.iloc[:, 
            df.columns.get_indexer(list(rename_dict.values()))]
        return df


class DataFrameMan(metaclass=Singleton):

    @staticmethod
    def change_date_type_to_datetime(dataframe, date_key):
        dataframe[date_key] = pd.to_datetime(dataframe[date_key])
        return dataframe
    
    @staticmethod
    def change_date_type_to_str(dataframe, date_key):
        dates = dataframe[date_key]
        dates = dates.apply(lambda x: x.strftime('%Y-%m-%d'))
        dataframe[date_key] = dates
        return dataframe
   
    @staticmethod 
    def _get_data_frame_by_group(dataframe, group_name, group_value):
        group_df = dataframe.groupby(group_name)
        if group_value in group_df.groups.keys():
            return group_df.get_group(group_value)
        return None

    @staticmethod
    def search_dataframe_value(dataframe, column_name, keyword):
        _filter = dataframe[column_name].str.contains(keyword)
        return dataframe[_filter]

    @staticmethod
    def _concat_dateframe_list(df_list):
        if not df_list:
            return None
        if len(df_list) == 1:
            return df_list[0]
        return pd.concat(df_list)
    
    @staticmethod
    def find_records_within_period(dataframe, date_key ,start_date, end_date):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        return dataframe[
            (dataframe[date_key] >= start_date) & (dataframe[date_key] < end_date)]
        
    def find_records_by_address(self, dataframe, address_columns, address):
        df_list = []
        for addr_col in address_columns:
            addr_df = self.search_dataframe_value(dataframe, addr_col, address)
            df_list.append(addr_df)
        return self._concat_dateframe_list(df_list)
        
if __name__ == "__main__":
    PandasHolder()
