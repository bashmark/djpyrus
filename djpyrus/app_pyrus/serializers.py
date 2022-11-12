from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ChainModel, RmsModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_staff', 'username', 'email']


class ChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChainModel
        fields = ['name', 'address', 'port', 'scheme', 'version', 'login', 'password']


class RmsSerializer(serializers.ModelSerializer):
    chain = serializers.StringRelatedField()

    class Meta:
        model = RmsModel
        fields = ['name', 'address', 'port', 'scheme', 'version', 'login', 'password', 'chain']
