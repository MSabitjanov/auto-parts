from django.shortcuts import render

from dj_rest_auth.registration.views import RegisterView

from .serializers import UserRegisterSerializer


class UserRegisterView(RegisterView):
    serializer_class = UserRegisterSerializer
