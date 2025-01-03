from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status,viewsets
from .serializers import (
    TaskSerializer,ChangePasswordSerializer,
    CustomUserSerializer,UserCreationSerializer,
    UserEmailTokenSerializer,UserLoginSerializer,
    UserResetPasswordSerializer,
    UserLoginResponseSerializer,
    PasswordTokenSerializer,LogoutSerializer
)
from .models import Task
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserCreationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        srz_data = UserCreationSerializer(data=request.data, context={'request':request})
        if srz_data.is_valid():
            serializer = srz_data.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserAccountActivateView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, user_id, token):
        data = {
            'user_id':user_id,
            'token':token
        }
        srz_data = UserEmailTokenSerializer(data=data)
        if srz_data.is_valid():
            user = srz_data.save()
            return Response(data={'message':'user activated !!', 'user':user.email},status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        srz_data = UserLoginSerializer(data=request.data)
        if srz_data.is_valid():
            response_data = {
                'user_id': srz_data.validated_data['user'].id,
                'username': srz_data.validated_data['user'].username,
                'email': srz_data.validated_data['user'].email,
                'access_token': srz_data.validated_data['access'],
                'refresh_token': srz_data.validated_data['refresh']
            }
            
            response_serializer = UserLoginResponseSerializer(data=response_data)
            response_serializer.is_valid(raise_exception=True)
            
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        srz_data = LogoutSerializer(data=request.data)
        if srz_data.is_valid():
            refresh_token = srz_data.validated_data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'you logged out successfully!!'}, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAttemptView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        srz_data = UserResetPasswordSerializer(data=request.data, context={'request':request})
        if srz_data.is_valid():
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, user_id, token):
        data = {
            'user_id':user_id,
            'token':token
        }
        srz_data = PasswordTokenSerializer(data=data)
        if srz_data.is_valid():
            return Response(data={"message":"valid token!!","data":srz_data.data},status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        srz_data = ChangePasswordSerializer(data=request.data)
        if srz_data.is_valid():
            user = srz_data.save()
            return Response(data={'message':'password changer','user':user.email}, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        # users = User.objects.all()
        srz_data = CustomUserSerializer(instance=request.user)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created')
    serializer_class = TaskSerializer