import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.core.mail import send_mail
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(blank=True,null=True)
    avatar = models.ImageField(blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def __str__(self):
        return f"{self.username} >> {self.email}"

    def send_email(self, request, action):
        """Send an email to this user.
        action=activate/reset-password"""
        reset_token = str(uuid.uuid4())
        self.token = reset_token
        self.save()
        reset_link = f"http://{request.get_host()}/{action}/{self.pk}/{reset_token}/"
        subject = f'{action} User Account'
        message = f'Click the link to for {action} : {reset_link}'
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [self.email])



class Task(models.Model):
    author = models.ForeignKey(CustomUser, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    context = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_done = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = ("Task")
        verbose_name_plural = ("Tasks")

    def __str__(self):
        return f"{self.author}  ::  {self.title}"