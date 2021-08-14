import sqlite3
from datetime import datetime


class Result:
    """
    分類結果
    """

    def __init__(self, auto_id, image_path, success, message, class_id, confidence, start, end):
        self.auto_id = auto_id
        self.image_path = image_path
        self.success = success
        self.message = message
        self.class_id = class_id
        self.confidence = confidence
        self.request_timestamp = start
        self.response_timestamp = end

    def __eq__(self, other):
        if isinstance(other, Result):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        ret = f'id:{self.auto_id}, image_path:{self.image_path}, success:{self.success}, '
        ret += f'message:{self.message}, class:{self.class_id}, confidence:{self.confidence}, '
        ret += f'request_timestamp:{datetime.fromtimestamp(self.request_timestamp)}, '
        ret += f'response_timestamp:{datetime.fromtimestamp(self.response_timestamp)}'
        return ret


class ResultModel:
    """
    DB操作用
    """
    table_name = 'ai_analysis_log'

    def __init__(self, db):
        self.db = db

    def save(self, result):
        """
        結果の格納

        Parameters
        ----------
        result: Result
            分類結果
        """
        self.create_table()
        conn = sqlite3.connect(self.db)
        try:
            cur = conn.cursor()
            sql = f'insert into {self.table_name}'
            sql += '(image_path, success, '
            sql += 'message, class, confidence, '
            sql += 'request_timestamp, response_timestamp) '
            sql += 'values(?, ?, ?, ?, ?, ?, ?)'
            cur.execute(sql, (result.image_path, str(result.success),
                              result.message, result.class_id, result.confidence,
                              result.request_timestamp, result.response_timestamp))
            conn.commit()
        finally:
            conn.close()

    def dump(self):
        """
        全行取得

        Yields
        -------
        Result
            分類結果
        """
        conn = sqlite3.connect(self.db)
        try:
            cur = conn.cursor()
            sql = f"select * from {self.table_name} order by request_timestamp"
            for r in cur.execute(sql):
                yield Result(r[0], r[1], r[2] == 'True', r[3], r[4], r[5], r[6], r[7])
        finally:
            conn.close()

    def create_table(self):
        """
        テーブル作成
        """
        conn = sqlite3.connect(self.db)
        try:
            cur = conn.cursor()
            sql = f'create table if not exists {self.table_name} '
            sql += '(id INTEGER PRIMARY KEY, image_path TEXT, success TEXT, '
            sql += 'message TEXT, class INTEGER, confidence REAL, '
            sql += 'request_timestamp INTEGER, response_timestamp INTEGER)'
            cur.execute(sql)
        finally:
            conn.close()

    def drop_table(self):
        """
        テーブル削除
        """
        conn = sqlite3.connect(self.db)
        try:
            cur = conn.cursor()
            sql = f'drop table if exists {self.table_name}'
            cur.execute(sql)
        finally:
            conn.close()
