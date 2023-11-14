from .models import *
from rest_framework import serializers
from django.utils.timesince import timesince
from datetime import datetime
from rest_framework.validators import UniqueValidator


class CommentSerializer(serializers.ModelSerializer):
    author=serializers.SerializerMethodField()
    time_passed=serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        author=None

        if "request" in self.context:
            author=self.context["request"].user

        validated_data.update({
            "author": author,
        })

        return Comment.objects.create(**validated_data)

    def get_author(self, obj):
        if obj.author:
            request=self.context.get("request")

            return{
                "profilePic": request.build_absolute_uri(obj.author.profilePic.url),
                'user_name': obj.author.user_name
            }
        return None
    
    def get_time_passed(self, obj):
        return timesince(obj.date_created)

class PostSerializer(serializers.ModelSerializer):
    
    comment=CommentSerializer(many=True, read_only=True)
    likes=serializers.SerializerMethodField()
    author=serializers.SerializerMethodField()
    is_liked=serializers.SerializerMethodField()
    time_passed=serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = '__all__'
    
    def create(self, validated_data):
        author=None

        if 'request' in self.context:
            author=self.context['request'].user

        validated_data.update({
            'author': author,
            'is_active': True
        })

        return Post.objects.create(**validated_data)
    
    def get_likes(self, obj):
        return obj.likes.count()
    

    def get_is_liked(self, obj):
        if 'request' in self.context:
            return obj.is_liked_by(self.context['request'].user)
        return False

    def get_author(self, obj):
        if obj.author:
            request=self.context.get('request')

            return{
                'profilePic': request.build_absolute_uri(obj.author.profilePic.url),
                'user_name':obj.author.user_name
            }
        return None
    
    def get_time_passed(self, obj):
        return timesince(obj.date_created)
    
class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = "__all__"