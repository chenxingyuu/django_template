from rest_framework import serializers

from .models import User


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password', 'groups', 'user_permissions']
