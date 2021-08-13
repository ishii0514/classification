import unittest
from unittest import mock
from classification import classifier as cl


class TestClassifier(unittest.TestCase):
    @mock.patch('classification.classifier.requests.post')
    @mock.patch('classification.classifier.time.time')
    def test_get_result(self, mock_time, mock_post):
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

        c = cl.Classifier('xxx/yyy.png')
        result = c.get_result()

        self.assertEqual(-1, result.auto_id)
        self.assertEqual('xxx/yyy.png', result.image_path)
        self.assertEqual(True, result.success)
        self.assertEqual('success', result.message)
        self.assertEqual(3, result.class_id)
        self.assertEqual(0.8683, result.confidence)
        self.assertEqual(1234567890, result.request_timestamp)
        self.assertEqual(1234567890, result.response_timestamp)

    @mock.patch('classification.classifier.requests.post')
    @mock.patch('classification.classifier.time.time')
    def test_get_result_false(self, mock_time, mock_post):
        mock_time.return_value = 1234567890.123
        mock_post.return_value = mock.Mock(status_code=200)
        mock_post.return_value.json.return_value = {
            'success': False,
            'message': 'Error:E50012',
            'estimated_data': {}
        }

        c = cl.Classifier('xxx/yyy.png')
        result = c.get_result()

        self.assertEqual(-1, result.auto_id)
        self.assertEqual('xxx/yyy.png', result.image_path)
        self.assertEqual(False, result.success)
        self.assertEqual('Error:E50012', result.message)
        self.assertEqual(None, result.class_id)
        self.assertEqual(None, result.confidence)
        self.assertEqual(1234567890, result.request_timestamp)
        self.assertEqual(1234567890, result.response_timestamp)
