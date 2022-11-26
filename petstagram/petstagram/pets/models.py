# pets/models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

from petstagram.core.model_mixins import StrFromFieldsMixin


UserModel = get_user_model()


class Pet(StrFromFieldsMixin, models.Model):
    str_fields = ('id', 'name')
    MAX_NAME_LENGTH = 30

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=False,
        blank=False,
    )

    personal_photo = models.URLField(
        null=False,
        blank=False,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    slug = models.SlugField(
        null=False,
        blank=True,
        unique=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )
    # def __init__(self, slug, *args, **kwargs):
    #     if not slug:
    #         slug = slugify(f'{self.id}-{self.name}')
    #
    #     super().__init__(slug=slug, *args, **kwargs)

    def save(self, *args, **kwargs):
        #Create/Update
        super().save(*args, **kwargs)

        #'if' is needed to make sure initail slug does not change with edits to object
        if not self.slug:
            self.slug = slugify(f'{self.id}-{self.name}')

        #Update
        return super().save(*args, **kwargs)

