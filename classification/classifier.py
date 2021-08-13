import requests
import time
from .models import ResultModel, Result
from . import settings


def save_classify(image_path):
    """
    画像を分類してDBへ保存

    Parameters
    ----------
    image_path: string
        画像ファイルパス
    """
    # class取得
    c = Classifier(image_path)
    result = c.get_result()
    # DBへセーブ
    m = ResultModel(settings.DATABASES['default'])
    m.save(result)

    print('Result:')
    print(result)


def show_history():
    """
    これまでの結果を表示
    """
    m = ResultModel(settings.DATABASES['default'])
    print('History:')
    for r in m.dump():
        print(r)


class Classifier:
    """
    分類結果を取得する
    """

    def __init__(self, image_path):
        self.image_path = image_path

    def get_result(self):
        """
        指定された画像ファイルの分類結果を返す

        Returns
        -------
        Result
            分類結果
        """
        res, start, end = _post(self.image_path)
        # res, start, end = _dummy_post(self.image_path)

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
    デバッグ用
    """
    start = int(time.time())  # 開始時間(unix time)
    time.sleep(1)
    end = int(time.time())  # 終了時間
    res = {
        'success': True,
        'message': 'success',
        'estimated_data': {
            'class': 3,
            'confidence': 0.8683
        }
    }
    return res, start, end
