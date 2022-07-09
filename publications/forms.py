from django import forms
from publications.models import Publication


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        exclude = ['user', 'moderation_status', 'published_at']
