from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .permissions import IsAuthorOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .models import *
from .serializers import *
import logging

logger = logging.getLogger(__name__)
class PostView(ModelViewSet):
    permission_classes=(IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    queryset = Post.objects.filter(is_active=True).order_by('-date_created')

    serializer_class = PostSerializer


    def get_queryset(self):
        queryset=self.queryset.all()
        hashtag=self.request.query_params.get("hashtag", None)

        if hashtag:
            pattern = r'(?:\s|^)#[({0})\-\.\_]+(?:\s|$)'.format(hashtag)
            queryset=queryset.filter(caption__iregex=pattern)
        
        return queryset

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post=self.get_object()
        obj, created=Like.objects.get_or_create(
            user=request.user,
            post=post,
        )

        if not created:
            obj.is_active= not obj.is_active
            obj.save()
        
        liked_or_unliked="liked" if obj.is_active else "unliked"

        return Response({
            "detail": "Successfuly {} post".format(liked_or_unliked)
        }, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=["delete"], permission_classes=[IsAuthenticated])
    def delete(self, request, postId):
        try:
            post = Post.objects.get(id=postId)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        if post.author == request.user:
            post.delete()
            return Response({"detail": "Post deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You are unauthorized to perform this operation"}, status=status.HTTP_403_FORBIDDEN)


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes=[IsAuthenticated, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset=self.queryset

        post=self.request.get_query_param("post", None)
        if post:
            return queryset.filter(post=post)
        return queryset
    
class LikePostView(APIView):
    permission_classes=[IsAuthenticated]


    def post(self, request, *args, **kwargs):
        post_id=kwargs.get("post_id")

        if not post_id:
            return Response({
                "detail": "Post id is not valid"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        post=get_object_or_404(Post, id=post_id)

        obj, created=Like.objects.get_or_create(
            user=request.user,
            post=post,
            
        )

        if created:
            user=LikeSerializer(instance=obj)
            user=user.data
            return Response(user, status=status.HTTP_201_CREATED)
        
        obj.is_active= not obj.is_active
        obj.save()

        user=LikeSerializer(instance=obj)
        user=user.data
        return Response(user, status=status.HTTP_200_OK)
        
