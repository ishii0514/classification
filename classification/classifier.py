import requests
import time
from .models import ResultModel, Result
from . import settings


def save_classify(image_path, dummy=False):
    """
    画像を分類してDBへ保存

    Parameters
    ----------
    image_path: string
        画像ファイルパス
    dummy: bool
        ダミーAPIの使用
    """
    # class取得
    c = Classifier(image_path, dummy)
    result = c.get_result()
    # DBへセーブ
    m = ResultModel(settings.DATABASES['default'])
    m.save(result)

    return result


def history():
    """
    これまでの結果を表示
    """
    m = ResultModel(settings.DATABASES['default'])
    return m.dump()


class Classifier:
    """
    分類結果を取得する
    """

    def __init__(self, image_path, dummy=False):
        self.image_path = image_path
        self.post = _dummy_post if dummy else _post

    def get_result(self):
        """
        指定された画像ファイルの分類結果を返す

        Returns
        -------
        Result
            分類結果
        """
        res, start, end = self.post(self.image_path)
        return Result(-1, self.image_path,
                      res['success'], res['message'],
                      int(res['estimated_data']['class']
                          ) if res['success'] else None,
                      float(res['estimated_data']['confidence']
                            ) if res['success'] else None,
                      start, end)


def _post(image_path):
    """
    ポスト処理を実行して結果と処理時間を返す

    Parameters
    ----------
    image_path: string
        画像ファイルパス

    Returns
    -------
    resoponse: Response
    start_time: int
    end_time: int
    """
    url = 'http://example.com/'
    payload = {'image_path': image_path}

    start = int(time.time())  # 開始時間(unix time)
    res = requests.post(url, data=payload)  # 例外はそのまま送出させる
    end = int(time.time())  # 終了時間
    return res.json(), start, end


def _dummy_post(image_path):
    """
    _post()のダミー関数。デバッグ用
    """
    start = int(time.time())  # 開始時間(unix time)
    time.sleep(1)
    end = int(time.time())  # 終了時間
    res = {
        'success': True,
        'message': 'success',
        'estimated_data': {
            'class': 2,
            'confidence': 0.5555
        }
    }
    return res, start, end
