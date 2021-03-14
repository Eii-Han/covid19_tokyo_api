import requests
import io

class PatientFileReader(object):

    def __init__(self, get_url:str , encoding:str ="utf-8"):

        res = requests.get(get_url)
        raw_content = res.content
        self._readable_cont = raw_content.decode(encoding)

    @property
    def get_csv_data(self):
        return self._readable_cont

    @property
    def get_csv_file_like_obj(self):
        return io.StringIO(self._readable_cont)

if __name__ == "__main__":

    f_obj = PatientFileReader('http://www.pref.kanagawa.jp/osirase/1369/data/csv/patient.csv', 'SHIFT-JIS')
    print(f_obj.csv_data)
        
