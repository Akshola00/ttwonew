from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from django.urls import path
from . import views

urlpatterns = [
    path('base', views.base, name='base' ),
    path('login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', views.RegisterView.as_view(), name='auth_register'),

]