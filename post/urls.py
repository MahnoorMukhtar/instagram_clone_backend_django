from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router=DefaultRouter()
router.register(r'post', PostView )
router.register(r'comment', CommentView)


urlpatterns = [

    path("like/<int:post_id>/", LikePostView.as_view()),   

] + router.urls
