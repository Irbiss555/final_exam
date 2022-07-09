from django.db import models
from django.db.models.deletion import get_candidate_relations_to_delete


class SoftDeletedManager(models.Manager):
    def get_queryset(self):
        return super(SoftDeletedManager, self).get_queryset().filter(is_deleted=False)


class IsDeletedMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeletedManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        delete_candidates = get_candidate_relations_to_delete(self.__class__._meta)
        if delete_candidates:
            for relation in delete_candidates:
                if (
                        relation.on_delete.__name__ == 'CASCADE'
                        and relation.one_to_many
                        and not relation.hidden
                ):
                    for item in getattr(self, relation.related_name).all():
                        item.delete()

        self.save(update_fields=['is_deleted', ])

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Publication(IsDeletedMixin):
