from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api import views


urlpatterns = [
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', views.LogoutView.as_view(), name='api_token_logout'),
    path(
        'publication/<int:pub_pk>/valid/',
        views.PublicationModerateValidAPIView.as_view(),
        name='publication_valid'),
    path(
        'publication/<int:pub_pk>/invalid/',
        views.PublicationModerateInValidAPIView.as_view(),
        name='publication_invalid',
    ),
]
