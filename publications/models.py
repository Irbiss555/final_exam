from django.contrib.auth import get_user_model
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
    MODERATION_CHOICES = [
        ('NOT_MODERATED', 'Not moderated'),
        ('VALID', 'Moderation valid'),
        ('INVALID', 'Moderation invalid'),
    ]

    category = models.ForeignKey(
        to='publications.Category',
        related_name='publications',
        on_delete=models.CASCADE,
        verbose_name='Category'
    )
    user = models.ForeignKey(
        to=get_user_model(),
        related_name='publications',
        on_delete=models.CASCADE,
        verbose_name='Author'
    )
    title = models.CharField(max_length=500, verbose_name='Title')
    text = models.TextField(max_length=2000, verbose_name='Text')
    image = models.ImageField(upload_to='publication_images', verbose_name='Image')
    price = models.price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Price',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Published')
    moderation_status = models.CharField(
        max_length=100, blank=True,
        verbose_name='Moderation status', choices=MODERATION_CHOICES, default='NOT_MODERATED'
    )

    def __str__(self):
        return f'Publication #{self.id} "{self.title}"'

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
