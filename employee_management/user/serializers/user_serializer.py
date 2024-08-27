from rest_framework import serializers
from ..models.user_models import User

class UserSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"