from rest_framework import serializers
from ...models import Service
from .subjects import SubjectSerializer


class ServiceSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'price', 'lessons_count', 'currency', 'subjects'
        ]
