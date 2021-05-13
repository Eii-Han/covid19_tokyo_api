# Developed Date; 2021-03-10
# Developer: Poon Ying Wai
# Description: Pythonでシングルトンパターン機能を提供するモジュール
#

class Singleton(type):
    """シングルトンクラス

    このクラスはシングルトンパターン機能の実装先クラスに以下の構文で定義すれば、
    シングルトンパターンの特性を有することが可能です。

    class ClassName(metaclass=Singleton):
    ※インポートを省略しました。

    Attributes:
        _instance: メタクラスとして持たせたクラスのインスタンス
    """

    _instance = None
    
    def __call__(cls, *args, **kwargs):
        """callメソッド

        callメソッドをオーバーライトして、インスタンス生成する前に、クラス側にインスタンスが存在しているかどうかを確認して、
        存在する場合、以前に生成したインスタンスを使用するようにクラスの動きを調整する

        Args:
            *args: 複数の引数をタプルとして受け取る
            **kwargs:複数のキーワード引数を辞書として受け取る

        Returns:
            対象クラスのインスタンス
        """
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance
