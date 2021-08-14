# About

- イメージファイルを指定すると、画像分類用 Web API で画像を分類し、結果を DB に保存する。
- コマンドラインから実行する。

# Environment

- python 3.9.6 で作成
- DB は sqlite3 を使用

# Usage

## 画像を分類する

### ダミーの API を使用して実行する場合

```
python3 -m classification cl -d /path/image_file.png
```

### Web API が実在する場合

```
python3 -m classification cl /path/image_file.png
```

## DB に格納された結果を参照する

```
python3 -m classification hs
```
