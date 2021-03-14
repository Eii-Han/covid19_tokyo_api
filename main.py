import pandas as pd
import datetime
from common.config import ConfigMan
from common.patient_file import PatientFileReader

conf_man = ConfigMan('config/config.json')

conf_json = conf_man.get_conf('kanagawa')
#conf_json = conf_man.get_conf('yokohama')

file_reader = PatientFileReader(conf_json['csv_url'], conf_json['encoding'])

df = pd.read_csv(file_reader.get_csv_file_like_obj, header=0)

df.rename(columns=conf_json.get('change_columns'), inplace=True)


date_df = df.groupby(conf_json['date_key'])

#today = datetime.date.today()
#today_str = f'{today.year:04}-{today.month:02}-{today.day:02}'
today_str = "2021-03-01"

if today_str in date_df.groups.keys():
    replaced_df = date_df.get_group(today_str)
    replaced_df = replaced_df.iloc[:, 
                    replaced_df.columns.get_indexer(
                    list(conf_json.get('change_columns').
                    values()))]
    records = replaced_df.to_dict(orient='records')
    count = len(replaced_df.index)
    import pprint
    print("count=", count)
    pprint.pprint(records)
else:
    print(None)
