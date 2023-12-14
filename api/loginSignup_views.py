from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

from .serializers import RegisterSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "user_info": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('login_api')
