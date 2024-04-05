from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import auth
from .auth import UserTokenObtainPairView

urlpatterns = [
    path('/info', auth.UserInfo.as_view()),
    path('/login', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
