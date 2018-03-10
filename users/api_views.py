import json
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from users.serializers import *
from cms.serializers import UserTableSerializer
from users.models import *
from cms.models import DepartmentTable, UserContribution, UserPost, UserComment
from cms.forms import UserContributionForm, UserPostForm
from django.contrib.auth.models import User


@api_view(['GET', 'POST'])
def users_list(request, format=None):
    """
    Return a list of users if GET, creates a new one if POST
    """
    if request.method == 'GET':
        users = User.objects.all()
        users_serialized = UserSerializer(users, many=True)
        return Response(users_serialized.data)
    elif request.method == 'POST':
        new_instance = UserSerializer(data=request.data)
        if not UserProfile.validate_name(request.data['username']):
            return Response(
                data={'error': 'اسم المستخدم مش مناسب.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not UserProfile.validate_mail(request.data['email'], 'api', True):
            return Response(
                data={'error': 'البريد الالكتروني مش صح.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if new_instance.is_valid():
            new_instance.save()
            return Response(new_instance.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_new_user(request, format=None):
    """Creates new user and return its token in response."""
    new_instance = UserSerializer(data=request.data)
    if not UserProfile.validate_name(request.data['username']):
        return Response(
            data={'error': 'اسم المستخدم مش مناسب.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not UserProfile.validate_mail(request.data['email'], 'api', True):
        return Response(
            data={'error': 'البريد الالكتروني مش صح.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if new_instance.is_valid():
        new_instance.save()
        return Response(
            data=new_instance.data,
            status=status.HTTP_201_CREATED)
    return Response(
        data={'error': new_instance.errors},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
def check_user_instance(request, format=None):
    """Checks if user is signed in, returns user.id if found, 0 otherwise."""
    username = request.POST.get('username', None)
    userpassword = request.POST.get('password', None)

    if username and userpassword:
        user = authenticate(username=username, password=userpassword)
        if user:
            return Response(
                data={'token': user.auth_token.key},
                status=status.HTTP_200_OK
            )
    return Response(
        data={'error': 'الاسم أو الباسورد مش صح!'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
def user_instance(request, pk, format=None):
    """
    Returns a user instance if GET, updates/deletes one due to pk if PUT or DELETE
    """
    try:
        user_instance = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serialized = UserSerializer(user_instance)
        return Response(user_serialized.data)

    elif request.method == 'PUT':
        user_serialized = UserSerializer(user_instance, data=request.data)
        if user_serialized.is_valid():
            user_serialized.save()
            return Response(user_serialized.data)
        return Response(user_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def universities_list(request, format=None):
    """
    Returns a list of universities if GET, 400-bad-request otherwise.
    """
    if request.method == 'GET':
        universities = University.objects.all()
        univrs_serialized = UniversitySerializer(universities, many=True)
        return Response(univrs_serialized.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def univerisity_instance(request, pk, format=None):
    """
    Returns a university instance if GET, 400-bad-request otherwise.
    """
    try:
        university_obj = University.objects.get(pk=pk)
    except University.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        university_serialized = UniversitySerializer(university_obj)
        return Response(university_serialized.data)


@api_view(['GET'])
def faculties_list(request, format=None):
    """
    Returns a list of faculties if GET, 400-bad-request otherwise.
    """
    if request.method == 'GET':
        faculties = Faculty.objects.all()
        faculties_serialized = FacultySerializer(faculties, many=True)
        return Response(faculties_serialized.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def faculties_university_list(request, uni_pk, format=None):
    """
    Returns a list of faculties that associates to specific university if GET, 400-bad-request otherwise.
    """
    try:
        university = University.objects.get(pk=uni_pk)
    except University.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        faculties = Faculty.objects.filter(university=university)
        faculties_serialized = FacultySerializer(faculties, many=True)
        return Response(faculties_serialized.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def faculty_instance(request, pk, format=None):
    """
    Returns a faculty instance if GET, 400-bad-request otherwise.
    """
    try:
        faculty_obj = Faculty.objects.get(pk=pk)
    except Faculty.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        faculties_serialized = FacultySerializer(faculty_obj)
        return Response(faculties_serialized.data)


@api_view(['GET'])
def departments_list(request, format=None):
    """
    Returns a list of departments if GET, 400-bad-request otherwise.
    """
    if request.method == 'GET':
        departments = Department.objects.all()
        departments_serialized = DepratmentSerializer(departments, many=True)
        return Response(departments_serialized.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def departments_faculty_list(request, fac_pk, format=None):
    """
    Returns a list of departments that associates to specific faculty if GET, 400-bad-request otherwise.
    """
    try:
        faculty = Faculty.objects.get(pk=fac_pk)
    except Faculty.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        departments = Department.objects.filter(faculty=faculty)
        departments_serialized = DepratmentSerializer(departments, many=True)
        return Response(departments_serialized.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def departments_instance(request, pk, format=None):
    """
    Returns a department instance if GET, 400-bad-request otherwise.
    """
    try:
        dep_obj = Department.objects.get(pk=pk)
    except Department.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        departments_serialized = DepratmentSerializer(dep_obj)
        return Response(departments_serialized.data)


@api_view(['GET'])
def universities_linked_instance(request, pk, format=None):
    """
    Returns a university instance with its linked faculties and departments if GET, 400-bad-request otherwise.
    """
    try:
        university_obj = University.objects.get(pk=pk)
    except University.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        university_serialized = UniversityLinkedSerializer(university_obj)
        return Response(university_serialized.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def main_table(request, user_id, format=None):
    """Returns dep table for given user instance on GET."""
    try:
        if request.user.profile:
            dep_table = DepartmentTable(request.user)
            tables_list = []
            for topic in dep_table.available_topics:
                try:
                    tables_list.append(topic.table.set_final_table())
                except:
                    # No table.
                    continue

            json_list = json.dumps(tables_list, ensure_ascii=False)
            return Response(json_list)

    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_table(request, user_id, format=None):
    """Returns user table for given user instance on GET."""
    try:
        if request.user.profile and request.user.profile.table:
            user_table = UserTableSerializer(request.user.profile.table)
            return Response(user_table.data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_contribution(request):
    """Add new contribution to speicifc topic."""
    if request.method == 'POST':
        contrib_form = UserContributionForm(
            request.POST,
            initial={
                'topic': request.POST.get('topic', -1),
                'user': request.user.id
            }
        )
        response = {}
        if contrib_form.is_valid():
            contrib_form.save()
            response['result'] = 'success'
            return Response(
                json.dumps(response)
            )
        else:
            response['result'] = 'failure'
            response['errors'] = contrib_form.errors
            return Response(
                json.dumps(response)
            )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_contribution_status(request):
    """changes the status of contribution from pending to approved/disapproved."""
    status = 3 if request.POST.get('accept_button', 0) else (2 if request.POST.get('ignore_button', 0) else 1)
    response = {}
    try:
        contribution = UserContribution.objects.get(id=request.POST.get('contribution_id', -1))
        contribution.status = status
        contribution.supervisior_id = request.user.id
        contribution.save()
        response['result'] = 'success'
        return Response(
            json.dumps(response)
        )
    except:
        # Invalid contribution.
        response['result'] = 'failure'
        return Response(
            json.dumps(response)
        )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_post(request):
    """Add new post to speicifc topic."""
    if request.method == 'POST':
        contrib_form = UserPostForm(request.POST,
                                    initial={'topic': request.POST.get('topic', -1), 'user': request.user.id})
        response = {}
        if contrib_form.is_valid():
            contrib_form.save()
            response['result'] = 'success'
            return Response(
                json.dumps(response)
            )
        else:
            response['result'] = 'failure'
            response['errors'] = contrib_form.errors
            return Response(
                json.dumps(response)
            )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_post_status(request):
    """changes the status of contribution from pending to approved/disapproved."""
    status = 3 if request.POST.get('accept_button', 0) else (2 if request.POST.get('ignore_button', 0) else 1)
    response = {}
    try:
        contribution = UserPost.objects.get(id=request.POST.get('post_id', -1))
        contribution.status = status
        contribution.supervisior_id = request.user.id
        contribution.save()
        response['result'] = 'success'
        return Response(
            json.dumps(response)
        )
    except:
        # Invalid contribution.
        response['result'] = 'failure'
        return Response(
            json.dumps(response)
        )


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_post_comments(request):
    """graps all post's comments."""

    post_id = request.GET.get('post_id', 0)
    if post_id:
        comments = UserComment.objects.filter(post_id=post_id, status=1)
        comments_serialized = CommentSerializer(comments, many=True)
        return Response(comments_serialized.data)
    else:
        return Response({})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_comment(request):
    """Add new comment to speicifc post."""
    response = {}
    try:
        user = request.user
        post = post = UserPost.objects.get(id=request.POST.get('post_id', 0))
        content = request.POST.get('comment_content', 0)
        if user and post and content:
            comment = UserComment.objects.create(
                post=post,
                user=user,
                content=content
            )
            response['result'] = 'success'
            return Response(
                json.dumps(response)
            )
    except:
        pass

    response['result'] = 'failure'
    return Response(
        json.dumps(response)
    )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def delete_comment(request):
    """deletes comment from speicifc post."""
    comment = request.POST.get('comment_id', 0)
    response = {}
    if comment and request.user.is_staff:
        try:
            comment = UserComment.objects.get(id=comment)
            comment.status = 0
            comment.supervisior_id = request.user.id
            comment.save()
            response['result'] = 'success'
            return Response(
                json.dumps(response)
            )
        except:
            pass

    # Invalid contribution.
    response['result'] = 'failure'
    return Response(
        json.dumps(response)
    )
