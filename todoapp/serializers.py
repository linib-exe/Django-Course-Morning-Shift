from rest_framework import serializers
from .models import TODO

class TODOSerializer(serializers.ModelSerializer):
    class Meta:
        model = TODO
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()