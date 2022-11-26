from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse

from petstagram.common.forms import PhotoCommentForm, SearchPhotosForm
from petstagram.common.models import PhotoLike
from petstagram.common.utils import get_photo_url
from petstagram.core.photo_utils import apply_likes_count, apply_user_liked_photo
from petstagram.photos.models import Photo
from pyperclip import copy


def index(request):
    search_form = SearchPhotosForm(request.GET)
    search_pattern = None
    if search_form.is_valid():
        search_pattern = search_form.cleaned_data['pet_name']

    photos = Photo.objects.all()

    if search_pattern:
        photos = photos.filter(tagged_pets__name__icontains=search_pattern)

    photos = [apply_likes_count(photo) for photo in photos]
    photos = [apply_user_liked_photo(photo) for photo in photos]

    context = {
        'photos': photos,
        'comment_form': PhotoCommentForm(),
        'search_form': search_form,
    }
    return render(request, 'common/home-page.html', context)


@login_required
def like_photo(request, photo_id):
    user_liked_photos = PhotoLike.objects.filter(photo_id=photo_id, user_id=request.user.pk,)

    if user_liked_photos:
        user_liked_photos.delete()
    else:
    # # Option 1
    # photo_like = PhotoLike(
    #     photo_id=photo_id,
    # )
    # photo_like.save()

    # Option 2
        PhotoLike.objects.create(
            photo_id=photo_id,
            user_id=request.user.pk,
        )

    # Option 3(Wrong -  additional call to db)
    # Correct, only if validation is needed
    # photo = Photo.objects.get(pk=photo_id)
    # PhotoLike.objects.create(
    #     photo=photo,
    # )

    return redirect(get_photo_url(request, photo_id))


@login_required
def share_photo(request, photo_id):
    photo_details_url = reverse('details photo', kwargs={
        'pk': photo_id,
    })
    copy(request.META['HTTP_HOST'] + photo_details_url)
    return redirect(get_photo_url(request, photo_id))


@login_required
def comment_photo(request, photo_id):
    photo = Photo.objects.filter(pk=photo_id) \
        .get()

    form = PhotoCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False) # Does not parse to DB
        comment.photo = photo
        comment.save()

    return redirect('index')
