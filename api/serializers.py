from rest_framework import serializers
from .models import Task
from .authentication import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()



class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.send_email(request, action='activate')
        return user
    
    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]
        if password != password2:
            raise serializers.ValidationError('mismatch passwords!!')
        return attrs


class UserEmailTokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField()
    
    def create(self, validated_data):
        user = User.objects.filter(pk=self.user_id)
        token = validated_data['token']
        if user.exists():
            user = user.first()
            if user.token != token:
                raise serializers.ValidationError("invalid token !!")
            user.is_active = True
            user.token = ''
            user.save()
            return user
        raise serializers.ValidationError('invalid user id !!')
    
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        user = authenticate(email, password)
        if user:
            if not user.is_active:
                raise serializers.ValidationError('check your emails and activate account first!!')
            refresh = RefreshToken.for_user(user=user)
            attrs['user'] = user
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
            return attrs
        raise serializers.ValidationError('incorrect password!!')


class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs['email']
        request = self.context.get('request')
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.first()
            user.send_email(request, action="reset-password")
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('user with provided email does not exists!!')


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password2 = serializers.CharField()
    
    def create(self, validated_data):
        user_id = self.context.get('user_id')
        password = validated_data.get('password2')
        user = User.objects.get(pk=user_id)
        user.set_password(password)
        user.save()
        return user
    
    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]
        if password != password2:
            raise serializers.ValidationError('mismatch passwords!!')
        return attrs

class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    class Meta:
        model = User
        fields = ["id", "last_login", "username", "is_active", "full_name", "email", "phone_number"]


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Task
        fields = "__all__"
        
    def create(self, validated_data):
        request = self.context.get('request')
        return Task.objects.create(author=request.user, **validated_data)