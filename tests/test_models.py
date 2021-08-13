import unittest
from classification.models import ResultModel
from classification.classifier import Result


class TestModels(unittest.TestCase):
    result_model = ResultModel('./tests/out/test.db')

    def setUp(self):
        self.result_model.drop_table()
        self.result_model.create_table()

    def test_save_dump(self):
        self.result_model.save(Result(-1, '/test/dummy.png', True,
                                      'success', 3, 0.8633, 1234567880, 1234567890))
        self.result_model.save(Result(-1, '/test/false.png', False,
                                      'Error:E50012', None, None, 1234567880, 1234567890))

        exps = [
            Result(1, '/test/dummy.png', True, 'success',
                   3, 0.8633, 1234567880, 1234567890),
            Result(2, '/test/false.png', False, 'Error:E50012',
                   None, None, 1234567880, 1234567890),
        ]
        for r, e in zip(self.result_model.dump(), exps):
            self.assertEquals(e, r)
