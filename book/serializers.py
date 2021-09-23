from rest_framework import serializers
from authentication.models import User

from .models import Book



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name")


class BookSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Book
        fields = ("id", "title", "owner", "authors")