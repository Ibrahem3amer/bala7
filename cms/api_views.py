from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cms.serializers import *
from cms.models import *

@api_view(['GET'])
def topics_list(request, format = None):
    """
    Return a list of topics using GET
    """
    if request.method == 'GET':
        topics              = Topic.objects.all()
        topics_serialized   = TopicSerializer(topics, many = True)
        return Response(topics_serialized.data)

@api_view(['GET'])
def topic_instance(request, pk, format = None):
    """
    Returns a topic instance if GET
    """
    try:
        topic_instance = Topic.objects.get(pk = pk)
    except Topic.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        topics_serialized = TopicSerializer(topic_instance)
        return Response(topics_serialized.data)