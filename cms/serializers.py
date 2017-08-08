from rest_framework import serializers
from cms.models import *
from users.models import Faculty
from django.contrib.auth.models import User

class TopicTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicTable
        fields = ('__all__')


class UserTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTable
        fields = ('__all__')


class TopicSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(read_only=True)
    faculty = serializers.PrimaryKeyRelatedField(read_only=True)
    table = TopicTableSerializer(read_only=True)
    
    class Meta:
        model   = Topic
        fields  = ('id', 'name', 'desc', 'term', 'department', 'faculty', 'table')

class FacultyTopicsSerializer(serializers.ModelSerializer):

    topics = serializers.SerializerMethodField('return_faculty_topics')

    class Meta:
        model   = Faculty
        fields  = ('name', 'topics')
    
    def return_faculty_topics(self, obj):
        return self.context.get('topics')


class MaterialSerializer(serializers.ModelSerializer):

    user    = serializers.PrimaryKeyRelatedField(read_only=True)
    topic   = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model   = Material
        fields  = ('__all__')
    

class TasksSerializer(serializers.ModelSerializer):

    user    = serializers.PrimaryKeyRelatedField(read_only=True)
    topic   = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model   = Task
        fields  = ('__all__')
