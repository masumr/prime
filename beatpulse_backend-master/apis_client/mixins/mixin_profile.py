from django.contrib.auth.models import Group
from rest_framework import serializers

from models.models import Profile


class _GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class MixinOwnProfileSerializer:
    groups = _GroupSerializer(many=True)
