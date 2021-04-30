import pandas as pd
import datetime
from common.config import ConfigMan
from common.patient_file import PatientFileReader
from common.pandas_man import PandasHolder, DataFrameMan

conf_man = ConfigMan('config/config.json')

# data_name = 'kanagawa'
data_name = 'yokohama'
conf_json = conf_man.get_conf(data_name)
#conf_json = conf_man.get_conf('yokohama')

file_reader = PatientFileReader(conf_json['csv_url'], conf_json['encoding'])

pd_holder = PandasHolder()
pd_holder.add_data(
    data_name, 
    file_reader.get_csv_file_like_obj,
    conf_json.get('change_columns'))

df = pd_holder.get_data(data_name, "dated_df")

df_man = DataFrameMan()

import pprint
df_man.change_date_type_to_datetime(df , conf_json["date_key"])
df = df_man.find_records_within_period(df, conf_json["date_key"], "2021-04-21", '2021-04-22')
df = df_man.find_records_by_address(df, conf_json["address_columns"], '横浜')
df = df_man.search_dataframe_value(df, 'age', '20代')
pprint.pprint(df_man.change_date_type_to_str(df, conf_json["date_key"]).to_dict(orient='records'))

# TODO グルーピング機能を実装



