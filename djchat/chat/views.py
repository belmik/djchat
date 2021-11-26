from typing import Any
from django.http.request import HttpRequest
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from chat.models import ChatMessage
from chat.serializers import ChatMessageSerializer


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    template_name = "chat/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class NewUserView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "chat/new_user.html"

    def form_valid(self, form: UserCreationForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    pass


class UserLoginView(LoginView):
    success_url = "/"
    redirect_authenticated_user = True
    template_name = "chat/login.html"


class MessagesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        messages = ChatMessage.objects.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
