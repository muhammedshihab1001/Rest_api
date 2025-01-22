from rest_framework import serializers
from django.contrib.auth.models import User
from people.models import Person

class Rigesterserializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # Password should not be readable

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Only include the fields you need

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already exists')
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email already exists')
        
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user  # Return the created user instance, not the validated data


class Loginserializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        # No need for a model here since it's just for authentication
        pass


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'