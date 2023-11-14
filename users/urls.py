from django.urls import path
from .views import RegisterUserView, ManageUserView, ManageAuthor, UserProfileUpdateView


urlpatterns = [
    path('register/', RegisterUserView.as_view()), 
    path('me/', ManageAuthor.as_view()), 
    path('users/<str:user_name>/', ManageUserView.as_view()),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
]
