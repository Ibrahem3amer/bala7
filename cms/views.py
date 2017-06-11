from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.urls import reverse
from cms.models import Topic, UserTopics

def restrict_access(request, topic_id):
    """
    Validates that request's user has a valid access to requested topic. 
    """

    # Filtering user's prefernces based on topic_id, using filter() on many-to-many relationship.
    user_topics = request.user.profile.topics.all()
    if user_topics.filter(id = topic_id).count() <= 0:
       raise Http404("This topic is not included in your topics list.") 

    return True

def get_topic(request, dep_id=-1, topic_id=-1):
    """
    Returns a specific topic with corresponding id. Returns 404 if topic wasn't accessible by user.
    """

    restrict_access(request, topic_id)

    try:
        topic = Topic.objects.get(pk = topic_id)
    except Topic.DoesNotExist:
        raise Http404("It doesn't exist!")

    # Validate that topic relates to department.
    if topic.department.id != int(dep_id):
        raise Http404("Incorrect department")


    return render(request, 'topics/get_topic.html', {'topic':topic})

def update_user_topics(request):
    """
    Accepts user request with topics from his faculty, calls update method. redirects to profile with status. 
    """
    if request.method == 'POST':
        user_topics = request.POST.getlist('chosen_list[]', None)
        if not user_topics:
            # TODO::Add message that inform user.
            return redirect(reverse('web_user_profile'))

        if(UserTopics.update_topics(request, user_topics)):
            # TODO::Add message that inform user of success.
            pass
        else:
            # TODO::Add message that inform user of failure.
            pass
        
        return redirect(reverse('web_user_profile'))

