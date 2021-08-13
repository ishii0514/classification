# About

- イメージファイルを指定すると、画像分類する API で画像を分類しその結果を DB に保存する。

# Environment

- python 3.9.6 で作成
- DB は sqlite3 を使用

# Usage

コマンドラインから使用する。

### 画像を分類する場合

```
python3 -m classification cl /path/image_file.png
```

### DB に格納された結果を参照する場合

```
python3 -m classification hs
```

### その他

画像分類の API は存在しないため、実際に動作させる際は`Classifier#get_result()`で`_post()`の代わりに`_dummy_post()`を使用してください。
