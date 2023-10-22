from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from authentication.models import User
from django.contrib.auth import authenticate

 
class UserRegistrationSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone', 'first_name', 'last_name']
        
    def create(self, clean_data):
        user_obj = User.objects.create_user(email=clean_data['email'], password=clean_data['password'])
        user_obj.username = clean_data['username']
        user_obj.save()
        return user_obj
    
    
class UserLoginSerilizer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise serializers.ValidationError('User not found')
        return user



class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = ['email', 'password']
        