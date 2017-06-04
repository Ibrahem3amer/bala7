from django.utils.functional import SimpleLazyObject
from cms.models import UserTopics

def add_nav_topics(request):
    """ Returns list of TopicNav objects that user can access """
    return {'nav_topics':UserTopics.get_user_topics_nav(request.user)}