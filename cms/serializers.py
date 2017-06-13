from rest_framework import serializers
from cms.models import *
from django.contrib.auth.models import User

class TopicSerializer(serializers.ModelSerializer):
    department  = serializers.PrimaryKeyRelatedField(read_only=True)
    faculty     = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model   = Topic
        fields  = ('id', 'name', 'desc', 'term', 'department', 'faculty')
