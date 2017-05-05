from rest_framework import serializers
from users.models import University

class UniversitySerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = University
        fields = ('id', 'name', 'bio', 'headmaster', 'rank')
        read_only_fields = ()