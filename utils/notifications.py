
class BaseNotification(object):

    def __init__(self, segment_name, segment_tag=None):
        self.segment_names = segment_name
        self.segment_tag = segment_tag

    def get_notification_headers(self):
        """
        Formulates the headers needed to send new notification.
        :return: Dict
        """
        pass

    def get_notification_details(self):
        """
        Formulates the segments needed to send new notification.
        :return: Dict
        """
        pass

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
        pass