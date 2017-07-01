from rest_framework import serializers
from cms.models import *
from users.models import Faculty
from django.contrib.auth.models import User

class TopicSerializer(serializers.ModelSerializer):
    department  = serializers.PrimaryKeyRelatedField(read_only=True)
    faculty     = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model   = Topic
        fields  = ('id', 'name', 'desc', 'term', 'department', 'faculty')

class FacultyTopicsSerializer(serializers.ModelSerializer):

    topics = serializers.SerializerMethodField('return_faculty_topics')

    
    def return_faculty_topics(self, obj):
        return self.context.get('topics')

    class Meta:
        model   = Faculty
        fields  = ('name', 'topics')