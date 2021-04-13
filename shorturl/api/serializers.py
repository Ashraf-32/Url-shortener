from shorturl.models import Url
from rest_framework import serializers
from django.contrib.auth.models import User

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'
        read_only_fields = ['short', 'owner', 'date', 'id']


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        write_only_fields = ['password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
        


