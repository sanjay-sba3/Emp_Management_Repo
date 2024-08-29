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
            # print(username, password)
             # Authenticate user using Django's built-in method
            user = authenticate(request, username=username, password=password)

            data = {}
            if user:
                # user_serializer = UserSerailizer(user).data
                # jwt tokenGenerate refresh token
                login_user = User.objects.get(username=username)
                access_token = AccessToken.for_user(user)
                data["username"] = user.username
                data["access_token"]=str(access_token)
                return Response(
                    {"message": "Logged in successfully", "data": data, "status": 200},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Username or password is incorrect", "data": [], "status": status.HTTP_401_UNAUTHORIZED},
                )
        except Exception as e:
            print(str(e))
            # raise ("login failed",400 )

            return Response(
                {"message": "Login failed", "data": [], "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
            )
        



class UserAPIView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        
        try:
            username = request.query_params.get("username", None) 
            data = {}
            if username:
                user = User.objects.get(username=username)
                username_serializer = UserSerailizer(user).data
                data["username"] = username_serializer["username"]
                data["email"] = username_serializer["email"]
                return Response({'message':"Success", 'data':data, 'status': status.HTTP_200_OK})
            else:
                return Response({"error":"User not found", "status" : status.HTTP_401_UNAUTHORIZED})
        except Exception as e:
            return Response(
                {"message": "Something went wrong", "data": [], "status":status.HTTP_500_INTERNAL_SERVER_ERROR},
                
            )
