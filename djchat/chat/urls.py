from django.urls import path

from . import views

urlpatterns = [
    path("new_user/", views.NewUserView.as_view(), name="new_user"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("messages/", views.MessagesAPIView.as_view(), name="messages"),
    path("", views.HomeView.as_view(), name="home"),
]
