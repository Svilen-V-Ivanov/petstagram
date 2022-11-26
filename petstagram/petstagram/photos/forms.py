from django import forms
from django.core.exceptions import ValidationError

from petstagram.common.models import PhotoLike, PhotoComment
from petstagram.core.form_mixins import DisabledFormMixin
from petstagram.photos.models import Photo


class PhotoBaseForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('publication_date', 'user', )


class PhotoCreateForm(PhotoBaseForm):
    pass


class PhotoEditForm(PhotoBaseForm):
    class Meta:
        model = Photo
        exclude = ('publication_date', 'photo')


class PhotoDeleteForm(DisabledFormMixin, PhotoBaseForm):
    disabled_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if commit:
            # Deleting relations is necessary when the on delete options for elements
            # are set to Restricted, which forces you to manually delete relations
            self.instance.tagged_pets.clear() # Deletes many-to-many relations
            PhotoLike.objects.filter(photo_id=self.instance.id) \
                .delete() # Deletes one-to-many relations
            PhotoComment.objects.filter(photo_id=self.instance.id) \
                .delete() # Deletes one-to-many relations
            self.instance.delete()

        return self.instance
