from django.shortcuts import render
from rest_framework import generics
from ..models.user_models import User
from rest_framework.response import Response
from ..serializers.user_serializer import UserSerailizer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
# Create your views here.


# this is login API
class LoginAPI(generics.GenericAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.data.get("username")
            password = request.data.get("password")
            print(user, password)
            user = User.objects.get(username = user)
            user_serializer = UserSerailizer(user).data
            # jwt tokenGenerate refresh token
            access_token = AccessToken.for_user(user)
            user_serializer["access_token"]=str(access_token)
            return Response({"message":"loged in", "data":user_serializer, "status" :200})
        except Exception as e:
            print(str(e))
            # raise ("login failed",400 )

            return Response({"message": "login failed","data": [], "status": 500})  
