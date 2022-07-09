from django.conf.urls.static import static
from django.urls import path

from core import settings
from publications.views import PublicationListView

app_name = 'publications'

urlpatterns = [
    path('', PublicationListView.as_view(), name='publication_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
