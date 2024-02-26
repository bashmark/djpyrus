from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ChainModel, RmsModel, RevisionModel, RemotesModel


class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevisionModel
        fields = ['revision']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_staff', 'username', 'email']


class ChainSerializer(serializers.ModelSerializer):
    remote = serializers.StringRelatedField(many=True)
    class Meta:
        model = ChainModel
        fields = ['name', 'address', 'port', 'scheme', 'version', 'login', 'password', 'remote']


class RmsSerializer(serializers.ModelSerializer):
    chain = serializers.StringRelatedField()
    remote = serializers.StringRelatedField(many=True)

    class Meta:
        model = RmsModel
        fields = ['name', 'address', 'port', 'scheme', 'version', 'login', 'password', 'chain', 'remote']


class RemoteSerializer(serializers.ModelSerializer):
    rms = serializers.PrimaryKeyRelatedField(read_only=True)
    chain = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RemotesModel
        fields = ['name', 'remote', 'password', 'rms', 'chain']
