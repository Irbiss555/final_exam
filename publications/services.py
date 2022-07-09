from publications.models import Publication


def publication_list_service(**filter_dict):
    if filter_dict:
        return Publication.objects.filter(moderation_status='VALID').filter(**filter_dict)
    return Publication.objects.filter(moderation_status='VALID')
