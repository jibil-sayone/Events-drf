from django.urls import path
from user.views import RegisterAPI, LoginAPI, UserListAPI, UserDetailAPI
from knox import views as knox_views


app_name = "user"

urlpatterns = [
      path('register', RegisterAPI.as_view()),
      path('login/', LoginAPI.as_view(), name='login'),
      path('logout/', knox_views.LogoutView.as_view(), name='logout'),
      path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
      path('users/', UserListAPI.as_view(), name="user_list"),
      path('users/<int:pk>/', UserDetailAPI.as_view(), name="user_list"),

]