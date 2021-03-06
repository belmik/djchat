from datetime import datetime
from time import time
from typing import Any

from chat.models import ChatMessage
from chat.serializers import ChatMessageSerializer
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from rest_framework import generics, permissions


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    template_name = "chat/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["page_size"] = settings.REST_FRAMEWORK["PAGE_SIZE"]
        today = datetime.today()
        context["cur_date"] = today.date().isoformat()
        context["cur_time"] = today.time().isoformat(timespec="minutes")
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

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if "anon" in request.GET:
            user, created = User.objects.get_or_create(username="anon")
            login(request, user)
            return redirect("home")
        return super().get(request, *args, **kwargs)


class MessagesAPIView(generics.ListAPIView):
    queryset = ChatMessage.objects.filter(post_time__lte=datetime.today()).order_by("-post_time")
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatMessageSerializer
