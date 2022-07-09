from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone


# Create your views here.
from publications.models import Publication


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return JsonResponse({'status': 'ok'})


class PublicationModerateValidAPIView(APIView):
    publication = None
    permission_classes = [IsAdminUser]

    def dispatch(self, request, *args, **kwargs):
        self.publication = get_object_or_404(Publication, pk=self.kwargs.get('pub_pk'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.publication.moderation_status = 'VALID'
        self.publication.published_at = timezone.now()
        self.publication.save()
        response = {'moderation_status': self.publication.get_moderation_status_display()}
        return JsonResponse(response, safe=False)


class PublicationModerateInValidAPIView(APIView):
    publication = None
    permission_classes = [IsAdminUser]

    def dispatch(self, request, *args, **kwargs):
        self.publication = get_object_or_404(Publication, pk=self.kwargs.get('pub_pk'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.publication.moderation_status = 'INVALID'
        self.publication.save()
        response = {'moderation_status': self.publication.get_moderation_status_display()}
        return JsonResponse(response, safe=False)
