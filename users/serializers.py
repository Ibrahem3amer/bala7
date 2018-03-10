from rest_framework import serializers
from users.models import *
from cms.models import UserComment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class UserProfileSerialzer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
        'university', 'faculty', 'department', 'level', 'gender', 'count_of_posts', 'count_of_replies', 'topics')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SVProfile
        fields = ('__all__')


class DepratmentSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Department
        fields = ('id', 'name', 'bio', 'team')


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'name', 'bio', 'university')


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('id', 'name', 'bio')


class DepratmentLinkedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'bio')


class FacultyLinkedSerializer(serializers.ModelSerializer):
    departments = DepratmentLinkedSerializer(many=True)

    class Meta:
        model = Faculty
        fields = ('id', 'name', 'bio', 'university', 'departments')


class UniversityLinkedSerializer(serializers.ModelSerializer):
    faculties = FacultyLinkedSerializer(many=True)

    class Meta:
        model = University
        fields = ('name', 'bio', 'faculties')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserComment
        fields = ('__all__')
