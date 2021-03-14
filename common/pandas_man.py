import pandas as pd
import datetime

from common.singleton import Singleton


class PandasHolder(metaclass=Singleton):

    def __init__(self):
        self._data_src = {}

    def add_data(self, data_name, data_obj, rename_dict):
        dt_now = datetime.datetime.now()
        now_str = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        self._data_src[data_name] = {}
        self._data_src[data_name]['_createdDate'] = now_str
        self._data_src[data_name]['dated_df'] = self._create_dataframe(data_obj, rename_dict)

    def get_data(self, data_name):
        if not self._data_src.get(data_name):
            return None
        return self._data_src[data_name]['dated_df']

    def get_updated_time(self, data_name):
        return self._data_src[data_name]['_createdDate']

    @staticmethod
    def _create_dataframe(data_obj, rename_dict):
        df = pd.read_csv(data_obj, header=0)
        df.rename(columns=rename_dict, inplace=True)
        df = df.iloc[:, 
            df.columns.get_indexer(list(rename_dict.values()))]
        return df


class DataFrameMan():

    def __init__(self):
        self._dataframe = None

    def set_data_frame(self, dataframe):
        self._dataframe = dataframe
   
    @staticmethod 
    def _get_data_frame_by_group(dataframe, group_name, group_value):
        group_df = dataframe.groupby(group_name)
        if group_value in group_df.groups.keys():
            return group_df.get_group(group_value)
        return None

    @staticmethod
    def _search_data_frame_value(dataframe, column_name, keyword):
        _filter = dataframe[column_name].str.contains(keyword)
        return dataframe[_filter]

    @staticmethod
    def _concat_dateframe_list(df_list):
        if not df_list:
            return None
        if len(df_list) == 1:
            return df_list[0]
        return pd.concat(df_list)

    def find_records_by_address_on_same_date(
            self, address, address_columns, date_key ,date_str):
        date_df = self._get_data_frame_by_group(
                      self._dataframe, date_key, date_str)
        if date_df.empty:
            return date_df
        df_list = []
        for addr_col in address_columns:
            addr_df = self._search_data_frame_value(date_df, addr_col, address)
            df_list.append(addr_df)
        return self._concat_dateframe_list(df_list)


if __name__ == "__main__":
    PandasHolder()
