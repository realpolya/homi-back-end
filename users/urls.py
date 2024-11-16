from .views import CreateUserView, LoginView, VerifyUserView
from django.urls import path


urlpatterns = [
    path('users/register/', CreateUserView.as_view(), name='register' ), 
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]