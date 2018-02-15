import requests
import json
from bala7.settings.base import secrets


class NotificationDevices(object):

    def __init__(self):
        self.app_id = secrets['onesignal_app_id']
        self.device_type = 8
        self.language = "en"
        self.tags = {
            "department": 3
        }

    def get_notification_headers(self):
        """
        Formulates the headers needed to query devices.
        :return: Dict
        """
        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }

    def get_device_details(self):
        """
        Builds the structure of the new device added to API.
        :return: Dict
        """
        pass

    def add_new_device(self):
        """
        Send POST request to add new device.
        :return: Dict of status.
        """
        pass


class BaseNotification(object):

    def __init__(self, segment_names, segment_tags=None):
        self.segment_names = segment_names
        self.segment_tags = segment_tags


    def get_notification_headers(self):
        """
        Formulates the headers needed to send new notification.
        :return: Dict
        """
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Basic "+secrets['onesignal_api_key']
        }

    def get_notification_details(self, en_message=None, ar_message=None):
        """
        Formulates the segments needed to send new notification.
        :return: Dict
        """
        en_message = en_message or "Hello, World!"
        ar_message = ar_message or "Hello, World!"
        payload = {
            "app_id": secrets['onesignal_app_id'],
            "contents": {
                "en": en_message,
                "ar": ar_message
            },
            "included_segments": self.segment_names
        }


    def create_notification(self):
        """
        Captures the saved instance and formulates it to be sent.
        :return: Dict
        """
        headers = self.get_notification_headers()
        payload = self.get_notification_details()

    def send_notification(self):
        """
        Launches a POST request to OneSignal API to send the notification.
        :return: Dict of status and errors.
        """

        headers = self.get_notification_headers()

        payload = {"app_id": "895c028d-2df9-4e48-8ba4-e3ed08a4ea8c",
                   "included_segments": ["All"],
                   "contents": {"en": "وسع وصلي ع النبي"}}

        req = requests.post("https://onesignal.com/api/v1/notifications", headers=headers, data=json.dumps(payload))

        print(req.status_code, req.reason)