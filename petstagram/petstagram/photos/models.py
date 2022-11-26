#photos/models.py
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from petstagram.core.model_mixins import StrFromFieldsMixin
from petstagram.pets.models import Pet
from petstagram.photos.validators import validate_file_less_than_5


UserModel = get_user_model()


class Photo(StrFromFieldsMixin, models.Model):
    str_fields = ('pk', 'photo', 'location')
    MAX_CHAR_LENGTH = 200
    MIN_CHAR_LENGTH = 10
    MAX_LOCATION_LENGTH = 30

    photo = models.ImageField(
        upload_to='pet_photos/',
        null=False,
        blank=True,
        validators=(validate_file_less_than_5,),
    )

    description = models.CharField(
        #DB validation
        max_length=MAX_CHAR_LENGTH,
        validators=(
            #Django/Python validation
            MinLengthValidator(MIN_CHAR_LENGTH),
        ),
        null=True,
        blank=True,
    )

    location = models.CharField(
        null=True,
        blank=True,
        max_length=MAX_LOCATION_LENGTH,
    )

    publication_date = models.DateField(
        blank=True,
        null=False,
        #Automatically sets current date on save
        auto_now=True,
    )

    tagged_pets = models.ManyToManyField(
        Pet,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )