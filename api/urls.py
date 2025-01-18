from django.urls import path
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tasks', views.TaskView,basename='task')


urlpatterns = [
    path('register/', views.UserCreationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('get-access-token/', views.GetAccessToken.as_view(), name='access-token'),
    path('activate-account/<int:user_id>/<str:token>/', views.UserAccountActivateView.as_view(), name='activate-account'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.ResetPasswordAttemptView.as_view(), name='password-reset-attempt'),
    path('password-reset/<int:user_id>/<str:token>/', views.ResetPasswordAttemptToView.as_view(), name='password-reset-attempt-1'),
    path('password-reset-confirm/', views.ResetPasswordView.as_view(), name='password-reset'),
    path('account-info/', views.UserInfoView.as_view(), name='user-info'),
]

urlpatterns += router.urls