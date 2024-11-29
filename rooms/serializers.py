from rest_framework import serializers
from .models import Room, AttachedFile

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'  # You can specify specific fields if needed instead of '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachedFile
        fields = '__all__'  # You can specify specific fields if needed instead of '__all__'
        def save(self, *args, **kwargs):
            return super().save(*args, **kwargs)
