from rest_framework import serializers
from .models import Task
from .authentication import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def create(self, validated_data):
        request = self.context.get("request")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.send_email(request, action="activate-account")
        return user

    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]
        if password != password2:
            raise serializers.ValidationError("mismatch passwords!!")
        return attrs


class UserEmailTokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.filter(pk=validated_data["user_id"])
        token = validated_data["token"]
        if user.exists():
            user = user.first()
            if user.token != token:
                raise serializers.ValidationError("invalid token !!")
            user.is_active = True
            user.token = ""
            user.save()
            return user
        raise serializers.ValidationError("invalid user id !!")


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        user = authenticate(email, password)
        if user:
            if not user.is_active:
                raise serializers.ValidationError(
                    "check your emails and activate account first!!"
                )
            refresh = RefreshToken.for_user(user=user)
            attrs["user"] = user
            attrs["refresh"] = str(refresh)
            attrs["access"] = str(refresh.access_token)
            return attrs
        raise serializers.ValidationError("incorrect password!!")


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserLoginResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs["email"]
        request = self.context.get("request")
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.first()
            user.send_email(request, action="password-reset")
            attrs["user"] = user
            return attrs
        raise serializers.ValidationError("user with provided email does not exists!!")


class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.get(
            pk=validated_data["user_id"], token=validated_data["token"]
        )
        password = validated_data.get("password2")
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]
        if password != password2:
            raise serializers.ValidationError("mismatch passwords!!")
        return attrs


class PasswordTokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(pk=attrs["user_id"])
        token = attrs["token"]
        if user.exists():
            user = user.first()
            if user.token != token:
                raise serializers.ValidationError("invalid token !!")
            attrs["user"] = user
            return attrs
        raise serializers.ValidationError("invalid user id !!")


class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "username",
            "is_active",
            "full_name",
            "email",
            "phone_number",
            "tasks",
        ]
        read_only_fields = [
            'id',
            'tasks',
        ]
    
    def get_tasks(self, obj):
        return TaskSerializer(instance=obj.tasks.all(), many=True, context=self.context).data


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        return Task.objects.create(author=request.user, **validated_data)
