from django.urls import path
from accounts.views import (
    LoginView,
    SignUpView,
    user_logout,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', user_logout, name='logout'),
]
