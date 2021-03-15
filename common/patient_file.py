import requests
import io

class PatientFileReader(object):
    """地域のデータファイルを読み込む機能を提供するクラス
    
    Attributes:
        _readable_cont: デコード済みの地域データ

    """
    def __init__(self, get_url:str , encoding:str ="utf-8"):
        """コンストラクタ
        
        ネット上に公開された情報を取得して、データをデコードして格納する
        """
        res = requests.get(get_url)
        raw_content = res.content
        self._readable_cont = raw_content.decode(encoding)

    @property
    def get_csv_data(self):
        """CSVフォーマットでデータ取得"""
        return self._readable_cont

    @property
    def get_csv_file_like_obj(self):
        """CSVファイルオブジェクト取得

        pandasライブラルのread_csvメソッドはファイルパスかファイルオブジェクトを受け取る仕様となっているので、
        変換機能を提供する。
        """
        return io.StringIO(self._readable_cont)


