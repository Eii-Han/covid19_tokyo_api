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
from builtins import staticmethod


class InvalidKeyError(Exception):
    """無効なキー名を使用されたときのエラー"""
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

    def add_data(self, data_name: str, data_obj: io.StringIO, rename_dict: dict, forced: bool = False) -> None:
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
        meta_keyで指定したデータのコピーを取得する
        
        Args:
            data_name: 地域の感染情報データの識別名
            meta_key: メタキー
        Returns:
            特定のデータ
        """
        if not self._data_src.get(data_name):
            return None
        meta_key = self._change_key(meta_key)
        # DataFrameがその後の処理で変更されることがないようにするため
        if isinstance(self._data_src[data_name].get(meta_key), pd.DataFrame):
            return self._data_src[data_name].get(meta_key).copy()
        return self._data_src[data_name].get(meta_key)

    @staticmethod
    def _change_key(meta_key: typing.Union[DataFrameMetaKey, str]) -> DataFrameMetaKey:
        """キーの値変更メソッド
        
        列挙型のDataFrameMetaKeyキー値を文字列型に変更する。
        
        Args:
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
    def _create_dataframe(data_obj: io.StringIO, rename_dict: dict) -> pd.DataFrame:
        """DataFrame生成メソッド

        CSV形式のデータオブジェクトからDataFrameを生成して、
        column名を再命名してからリターンする。
        ※再命名の理由は各自治体別で定義したカラム名を統一するため

        Args:
            data_obj: 対象地域のデータ
            rename_dict: 再命名対応づけ情報の辞書型
        Returns:
            データフレーム
        """
        df = pd.read_csv(data_obj, header=0)
        df.fillna("-", inplace=True)
        df.rename(columns=rename_dict, inplace=True)
        df = df.iloc[:, df.columns.get_indexer(list(rename_dict.values()))]
        # print(df)
        return df


class DataFrameMan(metaclass=Singleton):
    """DataFrameへの操作・処理を提供するクラス
    """
    @staticmethod
    def change_date_type_to_datetime(dataframe: pd.DataFrame, date_key: str) -> pd.DataFrame:
        """DataFrameの日付を日付型に変換するメソッド

        取得したデータフレームの日付を文字列型から日付型に変換する。

        Args:
            dataframe: データフレーム
            date_key: 日付のカラム名

        Returns:
            日付のデータ型が変換されたデータフレーム
        """
        dataframe.loc[:, date_key] = pd.to_datetime(dataframe[date_key])
        return dataframe

    @staticmethod
    def change_date_type_to_str(dataframe: pd.DataFrame, date_key: str) -> pd.DataFrame:
        """DataFrameの日付を文字列型に変換するメソッド

        取得したデータフレームの日付を日付型から文字列型に変換する。

        Args:
            dataframe: データフレーム
            date_key: 日付のカラム名

        Returns:
            日付のデータ型が変換されたデータフレーム
        """
        cdf = dataframe.copy()
        cdf.loc[:, date_key] = dataframe[date_key].dt.strftime('%Y-%m-%d')
        return cdf

    # @staticmethod
    # def _get_dataframe_by_group(
    #         dataframe: pd.DataFrame,
    #         group_name: str,
    #         group_value: typing.Any) -> typing.Union[pd.DataFrame, None]:
    #     group_df = dataframe.groupby(group_name)
    #     if group_value in group_df.groups.keys():
    #         return group_df.get_group(group_value)
    #     return None

    @staticmethod
    def search_dataframe_value(dataframe: pd.DataFrame, column_name: str, keyword: str) -> pd.DataFrame:
        """DataFrameから特定のキーワードを検索するメソッド

        DataFrameを受け取って指定したカラム名から、キーワードが含まれる行を検索して
        DataFrameとしてリターンする。

        Args:
            dataframe: データフレーム
            column_name: カラム名
            keyword:　検索したいキーワード

        Returns:
            検索後のデータフレーム
        """
        # print(f"keyword={keyword}")
        if not keyword:
            return dataframe
        _filter = dataframe[column_name].str.contains(keyword)
        return dataframe[_filter]

    @staticmethod
    def _concat_dataframe_list(df_list: list) -> typing.Union[pd.DataFrame, None]:
        """DataFrameを連結するメソッド

        それぞれ別のDataFrameをリスト型で受け取って、一つのデータフレームにまとめる。

        Args:
            df_list:

        Returns:
            連結後のデータフレーム
        """
        if not df_list:
            return None
        if len(df_list) == 1:
            return df_list[0]
        return pd.concat(df_list).drop_duplicates()

    @staticmethod
    def find_records_within_period(dataframe: pd.DataFrame, date_key: str, start_date: str,
                                   end_date: str) -> pd.DataFrame:
        """指定した日付の範囲内にDataFrameを検索するメソッド

        開始日付と終了日付を日時型に変換して、指定範囲内のDataFrameを検索して、
        DataFrameをリターンする。

        Args:
            dataframe: データフレーム
            date_key: 日付のキー名
            start_date: 開始日付
            end_date: 終了日付

        Returns:
            日付検索後のデータフレーム
        """
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        return dataframe[
            (dataframe[date_key] >= start_date) & (dataframe[date_key] <= end_date)]

    def find_records_by_address(
            self, dataframe: pd.DataFrame,
            address_columns: list, address: str) -> pd.DataFrame:
        """DataFrameを住所で検索するメソッド

        住所のカラム名をリストで受け取って、各住所カラム欄に対して検索をして、
        DataFrameをリターンする。

        Args:
            dataframe:　データフレーム
            address_columns:　住所カラム名のリスト
            address:　住所のキーワード

        Returns:
            住所検索後のデータフレーム
        """
        df_list = []
        for address_col in address_columns:
            address_df = self.search_dataframe_value(dataframe, address_col, address)
            df_list.append(address_df)
        return self._concat_dataframe_list(df_list)

    @staticmethod
    def limit_records(dataframe: pd.DataFrame, offset: int, limit: int) -> pd.DataFrame:
        """レコード数の取得を制限するメソッド

        Args:
            dataframe:
            offset:
            limit:

        Returns:

        """
        if offset is None and limit is None:
            return dataframe
        elif offset is None:
            return dataframe.iloc[:limit]
        elif limit is None:
            return dataframe.iloc[offset:]
        return dataframe.iloc[offset:offset + limit]

    @staticmethod
    def get_column_values(dataframe: pd.DataFrame) -> dict:
        results = dict()
        for c_name, items in dataframe.iteritems():
            for item in items:
                if not results.get(c_name):
                    results[c_name] = set()
                results[c_name].add(item)
            results[c_name] = list(results[c_name])
        return results
