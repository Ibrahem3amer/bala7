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

    def __init__(self, segment_names=None, segment_tags=None, messages=None):
        """
        Defines new instance of BaseNotification.
        :param segment_names: A list of strings that indicates the segments names.
        :param segment_tags: A dict of tags that indicates the key->value tags.
        :param messages: A dict of language->content that defines the message's content.
        """
        self.segment_names = segment_names or None
        self.segment_tags = [] or self.set_user_filters(segment_tags)
        self.messages = messages

    def set_user_filters(self, filters):
        """
        Formulates a dict of key->value to required format needed in OneSignal.
        :param filters: A dict of key->value that indicates filters to be applied.
        :return: Dict if filters has values, otherwise list.
        """
        try:
            for tag_key, tag_value in filters.items():
                self.segment_tags.append({
                    "field": "tag",
                    "key": tag_key,
                    "relation": "=",
                    "value": tag_value
                })
        except AttributeError:
            return []

    def get_notification_headers(self):
        """
        Formulates the headers needed to send new notification.
        :return: Dict
        """
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Basic "+secrets['onesignal_api_key']
        }
        return headers

    def get_notification_details(self):
        """
        Formulates the segments needed to send new notification.
        :return: Dict
        """
        messages = self.messages or {"en": "No content defined."}
        payload = {
            "app_id": secrets['onesignal_app_id'],
            "contents": messages,
            "included_segments": self.segment_names,
            "filters": self.segment_tags,
        }
        return payload

    def create_notification(self):
        """
        Formulate the notification to be sent to OneSignal API.
        :return: Dict
        """
        headers = self.get_notification_headers()
        payload = self.get_notification_details()
        request = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=headers,
            data=json.dumps(payload)
        )
        return request
