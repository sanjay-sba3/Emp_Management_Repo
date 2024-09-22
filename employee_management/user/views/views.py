import time
from django.shortcuts import render
from rest_framework import generics, status
from ..models.user_models import User
from rest_framework.response import Response
from ..serializers.user_serializer import UserSerailizer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from employee_management.project_utils.customexception import CustomException
from employee_management.project_utils.response import GetResponse
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
                login_user = User.objects.get(username=username)
                access_token = AccessToken.for_user(user)
                data["username"] = user.username
                data["access_token"]=str(access_token)
                time.sleep(4)
                return GetResponse(message= "Logged in successfully", data = [],status=status.HTTP_200_OK, type="Success")
            else:
                return GetResponse(message= "Username or password is incorrect", data = [],status=status.HTTP_401_UNAUTHORIZED, type="error")
 
        except Exception as e:
            print(str(e))
            # raise ("login failed",400 )

            return Response(
                {"message": "Login failed", "data": [], "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
            )
        



class UserAPIView(generics.GenericAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]


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

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            print(username, password)
            if not username or not password:
                raise CustomException("Either UserName or Passward not provided", status_code = status.HTTP_400_BAD_REQUEST)
            user = User.objects.filter(username=username)
            if user:
                raise CustomException("User with provided username already exists ", status_code=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create(username = username)
            user.set_password(password)
            user.save()
            user_data = UserSerailizer(user).data
            return GetResponse(status = status.HTTP_OK, type = "Success", message="Success", data=user_data)
        except CustomException as e:
            return GetResponse(status=e.status_code, type="error", message=str(e), data = [])
        except Exception as e:
            import traceback
            exc_traceback = e.__traceback__
            traceback_frames = traceback.extract_tb(exc_traceback)
            last_frame = traceback_frames[-1]
            function_name = last_frame.name
            print(f'Exception: {str(e)} , at line no : {e.__traceback__.tb_lineno} in function: {function_name}')
            return GetResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, type="error", message=str(e), data=[])
                