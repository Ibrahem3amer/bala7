import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.urls import reverse
from cms.models import Topic, UserTopics, Professor, DepartmentTable, UserTable, UserContribution, UserPost
from cms.forms import AddMaterialForm, UserContributionForm, UserPostForm

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


def add_weeks_to_materials(topic, secondary_materials=False):
    """
    Accepts number of weeks for specific topic, returns 1-based list that holds materials related to this week.
    """
    topic_weeks_range = topic.weeks
    materials_list = [0] * (topic_weeks_range+1)
    if secondary_materials:
        for i in range(1, topic_weeks_range):
            materials_list[i] = topic.secondary_materials.filter(week_number=i, status=3).all()
    else:
        for i in range(1, topic_weeks_range):
            materials_list[i] = topic.primary_materials.filter(week_number=i).all()

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
    user_faculty_departments = user_obj.profile.faculty.departments.all()
    true_topics = []
    for topic_id in list_of_topics_ids:
        try:
            true_topics.append(Topic.objects.get(id=topic_id))
        except:
            continue

    # Check if all topics in incoming request hold an accessible department id.
    for topic in true_topics:
        if topic.department not in user_faculty_departments:
            return False

    return True

@login_required
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

    # Get each week secondary materials.
    secondary_materials = add_weeks_to_materials(topic, True)

    # Get each week primary materials.
    materials = add_weeks_to_materials(topic, False)

    # Get user contribution form.
    user_contributon = UserContributionForm(initial={'topic':topic.id, 'user':request.user.id})

    # Get pending requests.
    pending_contributions = UserContribution.objects.filter(status=1, topic=topic)

    # Get discussion elements.
    post_request = UserPostForm(initial={'user': request.user.id, 'topic': topic.id})
    pending_posts = UserPost.objects.filter(status=1, topic=topic)
    posts = UserPost.objects.filter(topic=topic, status=3)

    return render(
        request,
        'topics/get_topic.html',
        {
            'topic':topic,
            'weeks_days': weeks,
            'weeks_materials': materials,
            'sec_materials': secondary_materials,
            'contribution_form': user_contributon,
            'pending_contributions': pending_contributions,
            'posts': posts,
            'post_request':post_request,
            'pending_posts':pending_posts,
        }
    )

@login_required
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

@login_required
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
        material_form   = AddMaterialForm(initial={'topic': topic.id})

    return render(request, 'add_material.html', {'add_material_form': material_form})


@login_required
def doctor_main_page(request, doctor_id):
    """
    Accepts GET, displays doctor's information. 
    """
    doctor = get_object_or_404(Professor, pk = doctor_id)
    if request.method == 'GET':
        return render(request, 'doctor/main.html', {'doctor': doctor})

@login_required
def dep_table_main(request):
    """Returns department table on GET."""
    if request.method == 'GET':
        try:
            # Grapping user department table.
            if request.user.profile:
                dep_table = DepartmentTable(request.user)
            return render(request, 'tables/table_main.html', {'table': dep_table})
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Please update your profile.')
            return redirect('web_user_profile')
    else:
        return redirect('home_user')

@login_required
def query_table(request):
    """Returns query results specified by user."""
    if request.method == 'POST':
        topics = request.POST.getlist('topics', None)
        professors = request.POST.getlist('professors', None)
        periods = request.POST.getlist('periods', None)
        days = request.POST.getlist('days', None)
        table = DepartmentTable(request.user)
        # results[0] -> table, results[1] -> choices
        results = table.query_table(request.user, topics, professors, periods, days)
        request.session['choices'] = results[1]

        return render(request, 'tables/query_results.html', {'table': results[0]})        

@login_required
def available_table(request):
    """Returns the main available table of department and user's topics."""
    if request.method == 'GET':
        try:
            # If user has no profile, redirect him to his profile.
            dep_table = DepartmentTable(request.user)
            topics = []
            for topic in dep_table.available_topics:
                try:
                    if topic.table:
                        topics.append(topic.table.set_final_table())
                except:
                    continue
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, 'Please update your profile.')
            return redirect('web_user_profile')

        return render(request, 'tables/available_table.html', {'table': topics})


@login_required
def user_table(request):
    """Returns user table on GET. Updates table on POST"""
    if request.method == 'GET':
        try:
            # If user has no table, display department table.
            if request.user.profile:
                user_table = request.user.profile.table
        except ObjectDoesNotExist:
            user_table = DepartmentTable(request.user)

        return render(request, 'tables/user_table.html', {'table': user_table})

    elif request.method == 'POST':
        # Checking for table existence. 
        choices = request.POST.getlist('choices[]', None) or request.session.get('choices', None)
        if len(choices) > 0:
            # Initiate a user table.
            user_table = UserTable.initiate_user_table(choices)
            # Create new Instance of user table.
            try:
                UserTable.objects.update_or_create(
                    user_profile=request.user.profile,
                    defaults={
                        'topics': user_table[0],
                        'places': user_table[1]
                    }
                )
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, 'Please update your profile.')
                return redirect('web_user_profile')
        else:
            messages.add_message(request, messages.ERROR, 'You did not choose any topics.')
        
        return redirect('web_user_table')

    else:
        return redirect('home_user')
