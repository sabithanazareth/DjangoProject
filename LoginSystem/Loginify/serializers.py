from .models import UserDetails
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserDetails
    fields = ['username', 'email', 'password']