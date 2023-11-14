from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from .serializers import UserCreateSerializer, UserInfoSerializer, FollowSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from post.permissions import IsAuthorOrReadOnly

User=get_user_model()
class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class=UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(
            data=request.data,
            context={"request": request}
            )

        if not serializer.is_valid():
            return Response({"errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
        serializer.save()  
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ManageUserView(generics.RetrieveAPIView):

    lookup_field='user_name'
    queryset=User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class=UserInfoSerializer

class ManageAuthor(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user
    
class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class=UserProfileSerializer
    permission_classes=[permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def update(self,request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class FollowUnFollowView(APIView):

    def get(self, request, user_name=None):
        from_user=self.request.user
        to_user=User.objects.get(user_name=user_name)
        follow=None

        if from_user.is_authenticated:
            if from_user in to_user.followers.all():
                follow=False
                from_user.following.remove(to_user)
                to_user.followers.remove(from_user)
            else:
                follow=True
                from_user.following.add(to_user)
                to_user.followers.add(from_user)
        
        return Response({'follow':follow})
    
    class UsersFollowersView(generics.ListAPIView):
        serializer_class=FollowSerializer
        permission_classes=(permissions.AllowAny,)

        def get_queryset(self, *args, **kwargs):
            user_name=kwargs('user_name')
            queryset=User.objects.get(user_name=user_name).followers.all()
            return queryset

    class UsersFollowingView(generics.ListAPIView):
        serializer_class=FollowSerializer
        permission_classes=(permissions.AllowAny,)

        def get_queryset(self, *args, **kwargs):
            user_name=kwargs('user_name')
            queryset=User.objects.get(user_name=user_name).following.all()
            return queryset



        
