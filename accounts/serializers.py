
from attr import fields
from pyrsistent import field
from rest_framework import serializers
from .models import *

class customuser_serializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields = '__all__' 

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email','username','password','first_name','last_name','number')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

class forget_password_serializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',) 


class Social_serializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields ='__all__'


class About_serializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields ='__all__'


class Profile_Pic_serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile_Pic
        fields ='__all__'


class Comment_serializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class User_Post_serializer(serializers.ModelSerializer):
    comment_set = Comment_serializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['post_name','tag_name','blog','post_header','post_content','images','document','likes','created_date','update_date','is_active','user','comment_set']
        

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['tag_name','blog_name','created_date','update_date','user']
        
    def create(self, validated_data):
        return Blog.objects.create(**validated_data)

