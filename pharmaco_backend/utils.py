import io
import os
import random
import string
import uuid

from PIL import Image
from django.conf import settings
from django.conf.global_settings import STATIC_ROOT
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.text import slugify
from rest_framework.pagination import PageNumberPagination


class PreModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


def random_string_generator(size=4, char=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(char) for _ in range(size))


def create_slug(instance, name=None, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(name)
        if len(slug) > 50:
            slug = slug[0:50]
    model = instance.__class__
    if model.objects.filter(slug=slug).exists():
        if len(slug) >= 46:
            slug = slug[0:45]
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(4)
        )
        return create_slug(instance, new_slug=new_slug)
    return slug


def random_int_with_n_digits_not_starting_with_zero(n):
    return random.randint(10 ** (n - 1) + 1, 10 ** n - 1)


def otpgen():
    return random_int_with_n_digits_not_starting_with_zero(6)


class PageNumberPaginationWithCount(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        response = super(PageNumberPaginationWithCount, self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        return response


def generate_image() -> InMemoryUploadedFile:
    img = Image.new('RGB', (100, 100), color=(73, 109, 137))
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG')
    img_file = InMemoryUploadedFile(img_io, None, ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) + ".jpg"
                                    , 'image/jpeg', img_io.getbuffer().nbytes, None)
    return img_file


def generate_medicine_image() -> InMemoryUploadedFile:
    # Get the path to the static folder
    static_folder = os.path.join(settings.BASE_DIR, "static/images")

    # Get a list of all the image files in the static folder
    image_files = [f for f in os.listdir(static_folder) if
                   f.endswith(".jpg") or f.endswith(".png") or f.endswith(".gif")]

    # Choose a random image file
    image_file = random.choice(image_files)

    img1 = Image.open(os.path.join(static_folder, image_file))
    img_io1 = io.BytesIO()
    img1.save(img_io1, 'JPEG')
    img_file = InMemoryUploadedFile(img_io1, None, ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) + ".jpg"
                                    , 'image/jpeg', img_io1.getbuffer().nbytes, None)
    return img_file

def generate_avatar_image() -> InMemoryUploadedFile:
    # Get the path to the static folder
    static_folder = os.path.join(settings.BASE_DIR, "static/imagesProf")

    # Get a list of all the image files in the static folder
    image_files = [f for f in os.listdir(static_folder) if
                   f.endswith(".jpg") or f.endswith(".png") or f.endswith(".gif")]

    # Choose a random image file
    image_file = random.choice(image_files)

    img1 = Image.open(os.path.join(static_folder, image_file))
    img_io1 = io.BytesIO()
    img1.save(img_io1, 'JPEG')
    img_file = InMemoryUploadedFile(img_io1, None, ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) + ".jpg"
                                    , 'image/jpeg', img_io1.getbuffer().nbytes, None)
    return img_file

