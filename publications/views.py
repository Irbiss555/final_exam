from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from publications.models import Publication
from publications.services import publication_list_service


class PublicationListView(ListView):
    template_name = 'publications/publication_list.html'
    model = Publication
    context_object_name = 'publications'

    def get_queryset(self):
        return publication_list_service()
