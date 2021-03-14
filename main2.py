import pandas as pd
import datetime
from common.config import ConfigMan
from common.patient_file import PatientFileReader
from common.pandas_man import PandasHolder, DataFrameMan

conf_man = ConfigMan('config/config.json')

data_name = 'kanagawa'
#data_name = 'yokohama'
conf_json = conf_man.get_conf(data_name)
#conf_json = conf_man.get_conf('yokohama')

file_reader = PatientFileReader(conf_json['csv_url'], conf_json['encoding'])

pd_holder = PandasHolder()
pd_holder.add_data(
    data_name, 
    file_reader.get_csv_file_like_obj,
    conf_json.get('change_columns'))

df = pd_holder.get_data(data_name)

df_man = DataFrameMan()
df_man.set_data_frame(df)
today_str = "2020-05-11"

target_df = df_man.find_records_by_address_on_same_date(
    "横浜市",
    conf_json["address_columns"],
    conf_json["date_key"],
    today_str)

if not target_df.empty:
    records = target_df.to_dict(orient='records')
    count = len(target_df.index)
    import pprint
    print("count=", count)
    pprint.pprint(records)
else:
    print("No records")
