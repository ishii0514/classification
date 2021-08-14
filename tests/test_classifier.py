import unittest
from unittest import mock
from classification import classifier as cl
from classification import settings


class TestClassifier(unittest.TestCase):
    @mock.patch('classification.classifier.requests.post')
    @mock.patch('classification.classifier.time.time')
    def test_get_result(self, mock_time, mock_post):
        """
        get_result 正常系のテスト
        """
        # timeとrequests.post部分をmock化
        mock_time.return_value = 1234567890.123
        mock_post.return_value = mock.Mock(status_code=200)
        mock_post.return_value.json.return_value = {
            'success': True,
            'message': 'success',
            'estimated_data': {
                'class': 3,
                'confidence': 0.8683
            }
        }

        c = cl.Classifier(
            '/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg')
        result = c.get_result()

        self.assertEqual(-1, result.auto_id)
        self.assertEqual(
            '/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg', result.image_path)
        self.assertEqual(True, result.success)
        self.assertEqual('success', result.message)
        self.assertEqual(3, result.class_id)
        self.assertEqual(0.8683, result.confidence)
        self.assertEqual(1234567890, result.request_timestamp)
        self.assertEqual(1234567890, result.response_timestamp)

    @mock.patch('classification.classifier.requests.post')
    @mock.patch('classification.classifier.time.time')
    def test_get_result_false(self, mock_time, mock_post):
        """
        get_result NGパターンのテスト
        """
        mock_time.return_value = 1234567890.123
        mock_post.return_value = mock.Mock(status_code=200)
        mock_post.return_value.json.return_value = {
            'success': False,
            'message': 'Error:E50012',
            'estimated_data': {}
        }

        c = cl.Classifier(
            '/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test_false.jpg')
        result = c.get_result()

        self.assertEqual(-1, result.auto_id)
        self.assertEqual(
            '/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test_false.jpg', result.image_path)
        self.assertEqual(False, result.success)
        self.assertEqual('Error:E50012', result.message)
        self.assertEqual(None, result.class_id)
        self.assertEqual(None, result.confidence)
        self.assertEqual(1234567890, result.request_timestamp)
        self.assertEqual(1234567890, result.response_timestamp)

    def test_get_result_dummy(self):
        """
        dummy_postのテスト
        """
        c = cl.Classifier(
            '/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test_dummy.jpg', True)
        result = c.get_result()

        self.assertEqual(-1, result.auto_id)
        self.assertEqual(
            '/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test_dummy.jpg', result.image_path)
        self.assertEqual(True, result.success)
        self.assertEqual('success', result.message)
        self.assertEqual(2, result.class_id)
        self.assertEqual(0.5555, result.confidence)

    @mock.patch('classification.classifier.requests.post')
    @mock.patch('classification.classifier.time.time')
    def test_save_classify(self, mock_time, mock_post):
        """
        save_classifyのテスト
        """
        # timeとrequests.post部分をmock化
        mock_time.return_value = 1234567890.123
        mock_post.return_value = mock.Mock(status_code=200)
        mock_post.return_value.json.return_value = {
            'success': True,
            'message': 'success',
            'estimated_data': {
                'class': 4,
                'confidence': 0.9999
            }
        }
        # DB設定をテスト用に変更
        settings.DATABASES['default'] = './tests/out/test.db'

        result = cl.save_classify(
            '/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg', False)

        self.assertEqual(-1, result.auto_id)
        self.assertEqual(
            '/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg', result.image_path)
        self.assertEqual(True, result.success)
        self.assertEqual('success', result.message)
        self.assertEqual(4, result.class_id)
        self.assertEqual(0.9999, result.confidence)
        self.assertEqual(1234567890, result.request_timestamp)
        self.assertEqual(1234567890, result.response_timestamp)
