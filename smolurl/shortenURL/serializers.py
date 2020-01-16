from rest_framework import serializers
from .models import URL


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields= ('id', 'address', 'created_at')