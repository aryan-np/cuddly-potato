from rest_framework import serializers

from .models import TodoModel

from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['username','email','password']
    
    def validate(self,data):
        username = data.get('username')
        if not User.objects.filter(username=username).exists():
            return data
        raise serializers.ValidationError("username alredy exists")
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
            
            
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModel
        exclude = ['owner']