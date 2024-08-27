from django.shortcuts import render
from rest_framework import generics, status
from ..models.user_models import User
from rest_framework.response import Response
from ..serializers.user_serializer import UserSerailizer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
# Create your views here.


# this is login API
class LoginAPI(generics.GenericAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            print(username, password)
             # Authenticate user using Django's built-in method
            user = authenticate(request, username=username, password=password)
            data = {}
            if user:
                # user_serializer = UserSerailizer(user).data
                # jwt tokenGenerate refresh token
                
                access_token = AccessToken.for_user(user)
                data["access_token"]=str(access_token)
                return Response(
                    {"message": "Logged in successfully", "data": data, "status": 200},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Username or password is incorrect", "data": [], "status": 401},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            print(str(e))
            # raise ("login failed",400 )

            return Response(
                {"message": "Login failed", "data": [], "status": 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )