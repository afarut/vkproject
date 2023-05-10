from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework import generics
from core.serializers import UserSerializer

User = get_user_model()


class UserApiView(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer