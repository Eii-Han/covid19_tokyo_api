from common.singleton import Singleton
from common.config import ConfigMan
from common.patient_file import PatientFileReader
from common.pandas_man import PandasHolder
from common.syslogman import SyslogMan
import collections

class Controller(metaclass=Singleton):

    def __init__(self):
        self._conf_man = ConfigMan('config/config.json')
        self._sm = SyslogMan('config/logger.yaml')
        self._dataframes = dict()

    def get_config_json(self, area: str):
        return self._conf_man.get_conf(area)

    def get_syslog_man(self):
        return self._sm

    def get_dataframe(self, area: str, force: bool):
        conf_json = self.get_config_json(area)
        file_reader = PatientFileReader(conf_json['csv_url'], conf_json['encoding'])

        pd_holder = PandasHolder()
        pd_holder.add_data(
            area,
            file_reader.get_csv_file_like_obj,
            conf_json.get('change_columns'),
            force
        )
        df = pd_holder.get_data(area, "dated_df")
        return df

    def flatten(self, args):
        for arg in args:
            if isinstance(arg, collections.abc.Iterable) and not isinstance(arg, (str, bytes)):
                yield from self.flatten(arg)
            else:
                yield arg