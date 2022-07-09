import typing

from django.db import models

from publications.models import Publication


def get_m2m_fields_data(model_class: [models.Model], data: typing.Dict) -> typing.Dict:
    m2m_fields_dict = {}
    for m2m_field in model_class._meta.many_to_many:
        if m2m_field.name in data:
            m2m_fields_dict[m2m_field.name] = data.pop(m2m_field.name)
    return m2m_fields_dict


def set_values_to_m2m_fields_of_object(
        obj: models.Model, m2m_fields_data_dict: typing.Dict) -> None:
    for field_name, value in m2m_fields_data_dict.items():
        getattr(obj, field_name).set(value)


def publication_list_service(**filter_dict):
    if filter_dict:
        return Publication.objects.filter(moderation_status='VALID').filter(**filter_dict)
    return Publication.objects.filter(moderation_status='VALID')


def publication_create_service(**data):
    m2m_fields_dict = get_m2m_fields_data(Publication, data)
    publication = Publication.objects.create(**data)
    set_values_to_m2m_fields_of_object(publication, m2m_fields_dict)
    return publication


def publication_update_service(publication, **data):
    m2m_fields_dict = get_m2m_fields_data(Publication, data)
    set_values_to_m2m_fields_of_object(publication, m2m_fields_dict)
    for field, value in data.items():
        setattr(publication, field, value)
    publication.moderation_status = "NOT_MODERATED"
    publication.save()
    return publication


