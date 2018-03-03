from test_plus.test import APITestCase, TestCase
from utils.notifications import BaseNotification


class TestAPIIntegeration(TestCase):

    def setUp(self):
        self.segments = ['test_users']
        self.messages = {
            "en": "this is test message content",
            "ar": "هذه رسالة تجربة"
        }
        self.notification = BaseNotification(segment_names=self.segments, messages=self.messages)

    def test_live_api_integeration_with_segments_only(self):
        """Assert that API will connect to OneSignal and return 200"""
        # Test setup
        # Test body
        result = self.notification.create_notification()
        # Test assertion
        self.assertEqual(result.reason, 'OK')
        self.assertIn(result.status_code, [200, 201, 202])

    def test_live_api_integeration_with_customized_message(self):
        """Assert that API will connect to OneSignal and return 200"""
        # Test setup
        self.messages["en"] = "Customized message!"
        another_notification = BaseNotification(self.segments, self.messages)
        # Test body
        result = self.notification.create_notification()
        # Test assertion
        self.assertEqual(result.reason, 'OK')
        self.assertIn(result.status_code, [200, 201, 202])

    def test_live_api_integeration_with_segments_and_tags(self):
        """Asserts that API will connect to OneSignal and return 200"""
        self.notification.set_user_filters({"department": "FCIMU"})
        result = self.notification.create_notification()
        # Test assertion
        self.assertEqual(result.reason, 'OK')
        self.assertIn(result.status_code, [200, 201, 202])

    def test_live_api_integeration_with_missing_segments(self):
        """Asserts that API will connect to OneSignal and return 400"""
        invalid_notification = BaseNotification()
        result = invalid_notification.create_notification()
        # Test assertion
        self.assertEqual(result.reason, 'Bad Request')
        self.assertIsNotNone(result.json()['errors'])
        self.assertIn(
            'You must include which players, segments, or tags you wish to send this notification to.',
            result.json()['errors']
        )
        self.assertIn(result.status_code, [400, 401, 402])

    def test_live_api_integeration_with_wrong_tags_format(self):
        """Asserts that API will connect to OneSignal and return 200"""
        invalid_notification = BaseNotification(
            segment_names=['test_users'],
            segment_tags=['invalid_one']
        )
        result = invalid_notification.create_notification()

        # Test assertion
        self.assertEqual(result.reason, 'OK')
        self.assertIn(result.status_code, [200, 201, 202])