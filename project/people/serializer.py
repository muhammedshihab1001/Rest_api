
from rest_framework import serializers
from people.models import Person
from django.contrib.auth.models import User

class Rigesterserializer(serializers.ModelSerializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'
    
    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('username already exists')
            
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('email already exists')
        return data
    def create(self,vaildated_date):
        user=User.objects.create(username=vaildated_date['username'],email=vaildated_date['email'])
        user.set_password(vaildated_date['password'])
        user.save()
        return vaildated_date


class loginserializer(serializers.ModelSerializer):
    username=serializers.CharField()
    password=serializers.CharField()
    class Meta:
        model = User
        fields = '__all__'

class Personserializer(serializers.ModelSerializer):
    class Meta:
        model=Person
        fields='__all__'