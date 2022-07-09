from django.conf.urls.static import static
from django.urls import path

from core import settings
from publications import views

app_name = 'publications'

urlpatterns = [
    path('', views.PublicationListView.as_view(), name='publication_list'),
    path('create/', views.PublicationCreateView.as_view(), name='publication_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
