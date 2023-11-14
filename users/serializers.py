from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from post.serializers import PostSerializer
from post.models import Post

User = get_user_model()
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    profilePic=serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('user_name','first_name', 'last_name', 'email','password', 'profilePic')

    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user

    def get_profilePic(self, obj):

        if 'request' in self.context:
            return self.context['request'].build_absolute_uri(obj.profilePic.url)
        return None

    
class UserInfoSerializer(serializers.ModelSerializer):

    num_of_posts=serializers.SerializerMethodField()
    post=serializers.SerializerMethodField()
    followed_by_request_user=serializers.SerializerMethodField()
    num_of_followers=serializers.SerializerMethodField()
    num_of_following=serializers.SerializerMethodField()

    class Meta:
        model= User
        fields = '__all__'
        
        extra_kwargs={'password':{
                                    'write_only': True,
                                    'min_length': 8
                                }}
        
    def update(self, instance, validated_data):
            password=validated_data.pop('password', None)

            if password:
                instance.set_password(password)

            for(key, value) in validated_data.items():
                setattr(instance, key, value)

            instance.save()
            return instance

    def get_num_of_followers(self, obj):
        return obj.num_of_followers()
    
    def get_num_of_following(self, obj):
        return obj.num_of_following()


    def get_num_of_posts(self, obj):
        return Post.objects.filter(author=obj).count()

    def get_post(self, obj):
        
        request= self.context.get('request')
        user_post=obj.post_set.filter(is_active=True).order_by("-date_created")
        if user_post.exists():
            return PostSerializer(user_post,many=True, context={"request": request}).data
        else:
            return None
            
    def get_followed_by_request_user(self, obj):
        user=self.context['request'].user
        return user in obj.followers.all()
    
class FollowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model: User
        fields=('user_name','profilePic')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields=('bio', 'profilePic', 'first_name', 'last_name')
