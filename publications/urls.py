from django.conf.urls.static import static
from django.urls import path

from core import settings
from publications import views

app_name = 'publications'

urlpatterns = [
    path('', views.PublicationListView.as_view(), name='publication_list'),
    path('create/', views.PublicationCreateView.as_view(), name='publication_create'),
    path('<int:pk>/', views.PublicationDetailView.as_view(), name='publication_detail'),
    path('<int:pk>/update/', views.PublicationUpdateView.as_view(), name='publication_update'),
    path('<int:pk>/delete/', views.PublicationDeleteView.as_view(), name='publication_delete'),
    path('to/moderate/', views.PublicationListToModerate.as_view(), name='publication_list_to_moderate'),
    path('<int:pk>/to/moderate/', views.PublicationDetailToModerateView.as_view(), name='publication_detail_to_moderate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
