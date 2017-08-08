import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from cms.serializers import *
from cms.models import *
from cms.views import restrict_access, within_user_domain, add_weeks_to_materials
from users.models import Faculty, Department, UserProfile

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
@permission_classes((IsAuthenticated,))
def topic_instance(request, pk, format = None):
    """
    Returns a topic instance if GET
    """

    # Validates that user has an access on this instance. 
    if not restrict_access(request, pk):
        return Response(status = status.HTTP_400_BAD_REQUEST)

    try:
        topic_instance = Topic.objects.get(pk = pk)
    except Topic.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        topics_serialized = TopicSerializer(topic_instance)
        return Response(topics_serialized.data)

@api_view(['GET'])
def topic_faculty(request, fac_id, format = None):
    """
    Returns all topics associated with specific faculty as {'dep':{topic1, topic2, ...etc}, 'dep2':{topic1, topic2, ...ect}, ...etc}
    """

    # Check the existence of faculty id.
    try:
        faculty = Faculty.objects.get(pk = fac_id)
    except Faculty.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    departments = faculty.departments.all()

    if departments:
        # Buliding the result dictionary.
        # {'dep':{topic1, topic2, ...etc}, 'dep2':{topic1, topic2, ...ect}, ...etc}
        departments_topics = {}
        for dep in departments:
            departments_topics[dep.name] = Topic.objects.filter(department = dep).values('id', 'name')

        topics_serialized = FacultyTopicsSerializer(faculty, context = {'topics': departments_topics})
        return Response(topics_serialized.data)

    return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def user_topics(request, format = None):
    """
    Returns list of user's topics if get, Update user's selection if post.
    """

    if request.method == 'GET':
        topics              = request.user.profile.topics
        topics_serialized   = TopicSerializer(topics, many = True)
        return Response(topics_serialized.data)

    if request.method == 'POST':
        user_choices = request.POST.getlist('chosen_list[]', None)
        if not user_choices or not within_user_domain(request.usser, user_choices):
            return Response(status = status.HTTP_400_BAD_REQUEST)

        if(UserTopics.update_topics(request, user_topics)):
            return Response(status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def materials_list(request, topic_id, format = None):
    """
    Return a list of materials related to specific topic using GET
    """

    # Validates that user has an access on this instance. 
    if not restrict_access(request, topic_id):
        return Response(status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        try:
            topic_instance = Topic.objects.get(pk = topic_id)
        except Topic.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        materials               = Material.objects.filter(topic_id = topic_id).all()
        materials_serialized    = MaterialSerializer(materials, many = True)
        return Response(materials_serialized.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def tasks_list(request, format = None):
    """
    Return a list of tasks whose deadlines are to be met.
    """
    if request.method == 'GET':
        tasks               = Task.get_closest_tasks(request)
        tasks_serialized    = TasksSerializer(tasks, many = True)
        return Response(tasks_serialized.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def query_dep_table(request, format = None):
    """Query dep table using given paramaters via POST."""
    
    topics = request.POST.getlist('topics', None)
    professors = request.POST.getlist('professors', None)
    periods = request.POST.getlist('periods', None)
    days = request.POST.getlist('days', None)
    table = DepartmentTable(request.user)
    
    # results[0] -> table, results[1] -> choices
    results = table.query_table(request.user, topics, professors, periods, days)
    request.session['choices'] = results[1]

    if(results[0]):
        json_table = json.dumps(results[0])
        return Response(json_table)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)