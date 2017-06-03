from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from cms.models import Topic

def get_topic(request, dep_id, topic_id):
    """
    Returns a specific topic with corresponding id. Returns 404 if topic wasn't accessible by user.
    """

    # Validate that user has access to this part. 
    if request.user.profile.department.id != int(dep_id):
        raise Http404("You cannot see this!")

    # TODO: Validate that topic is in user's perefrences.

    try:
        topic = Topic.objects.get(pk = topic_id)
    except Topic.DoesNotExist:
        raise Http404("It doesn't exist!")

    # Validate that topic relates to department.
    if topic.department.id != int(dep_id):
        raise Http404("Incorrect department")


    return render(request, 'topics/get_topic.html', {'topic':topic})	
