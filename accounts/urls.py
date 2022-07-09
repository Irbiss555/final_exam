from django.urls import path

from django.contrib.auth.views import LogoutView

from accounts.views import LoginUserView, RegisterView, UserDetailView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='user_create'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user_detail'),
]
