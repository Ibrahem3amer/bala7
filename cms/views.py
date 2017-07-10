from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.urls import reverse
from cms.models import Topic, UserTopics
from cms.forms import AddMaterialForm

def add_weeks_to_range(topic_weeks_range):
    """
    Accepts range of weeks for specific topic, returns dictionary of this range size that maps week days.
    """
    weeks = [
        'الأسبوع الأول',
        'الأسبوع الثاني',
        'الأسبوع الثالث',
        'الأسبوع الرابع',
        'الأسبوع الخامس',
        'الأسبوع السادس',
        'الأسبوع السابع',
        'الأسبوع الثامن',
        'الأسبوع التاسع',
        'الأسبوع العاشر',
        'الأسبوع الحادي عشر',
        'الأسبوع الثاني عشر',
    ]


    weeks = weeks[:topic_weeks_range]
    return weeks


def add_weeks_to_materials(topic):
    """
    Accepts number of weeks for specific topic, returns 1-based list that holds materials related to this week.
    """
    topic_weeks_range = topic.weeks
    materials_list = [0] * (topic_weeks_range+1)
    for i in range(1, topic_weeks_range):
        materials_list[i] = topic.primary_materials.filter(week_number = i).all()

    return materials_list


def restrict_access(request, topic_id):
    """
    Validates that request's user has a valid access to requested topic. 
    """

    # Filtering user's prefernces based on topic_id, using filter() on many-to-many relationship.
    user_topics = request.user.profile.topics.all()
    if user_topics.filter(id = topic_id).count() <= 0:
        return False

    return True

def within_user_domain(user_obj, list_of_topics_ids):
    """
    Validates that topics are within the same faculty of user's.
    """
    user_faculty_departments = user_obj.profile.faculty.departments.all().values_list('id', flat=True)
    request_topics           = Topic.objects.filter(id__in = list_of_topics_ids).values_list('department', flat=True)

    # Check if all topics in incoming request hold an accessible department id.
    for topic in request_topics:
        if topic not in user_faculty_departments:
            return False

    return True

def get_topic(request, dep_id=-1, topic_id=-1):
    """
    Returns a specific topic with corresponding id. Returns 404 if topic isn't accessible by user.
    """
    try:
        topic = Topic.objects.get(pk = topic_id)
    except Topic.DoesNotExist:
        raise Http404("It doesn't exist!")

    # User has no access to this topic.
    if not restrict_access(request, topic_id):
        raise Http404("Access denied.")

    # Validates that topic relates to department.
    if topic.department.id != int(dep_id):
        raise Http404("Incorrect department.")

    # Get dictionary of current size of weeks.
    weeks = add_weeks_to_range(topic.weeks)

    # Get each week materials.
    materials = add_weeks_to_materials(topic)

    return render(request, 'topics/get_topic.html', {'topic':topic, 'weeks_days': weeks, 'weeks_materials': materials})

def update_user_topics(request):
    """
    Accepts user request with topics from his faculty, calls update method. redirects to profile with status. 
    """
    if request.method == 'POST':
        user_topics = request.POST.getlist('chosen_list[]', None)
        # Validates that user has an access to these topics.
        if not user_topics or not within_user_domain(request.user, user_topics):
            messages.add_message(request, messages.ERROR, 'You chose empty or unavailabe topics')
            return redirect(reverse('web_user_profile'))


        if(UserTopics.update_topics(request, user_topics)):
            messages.add_message(request, messages.SUCCESS, 'Topics updated successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Select valid topics')

        return redirect(reverse('web_user_profile'))

def add_material(request):
    """
    Accepts POST, GET requets. Add new material if POST, collecting user and topic details from request if GET.
    """
    if request.method == 'POST':
        material_form = AddMaterialForm(request.POST)
        if material_form.is_valid():
            material_form.save()
            return redirect('home_user')
    else:
        # Initiate new form, gather user and topic from request details. 
        user            = request.user
        request_url     = '/topics/4/7'.split('/')
        topic           = get_object_or_404(Topic, pk = request_url[3])
        material_form   = AddMaterialForm(initial={'user': user, 'topic': topic})

    return render(request, 'add_material.html', {'add_material_form': material_form})

