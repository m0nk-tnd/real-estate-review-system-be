from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from images.models import Image, ImageAlbum


class ImageAlbumModelTest(TestCase):
    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg',
                                      content=b'',
                                      content_type='image/jpeg')
        self.album = ImageAlbum.objects.create(name='MyAlbum')
        self.image = Image.objects.create(name='my img', image=self.img, album=self.album)

    def test_name_label(self):
        album = ImageAlbum.objects.get(id=self.album.id)
        field_label = album._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_str(self):
        album = ImageAlbum.objects.get(id=self.album.id)
        expected = f"{album.name}"
        self.assertEquals(expected, str(album))

    def test_get_images(self):
        album = ImageAlbum.objects.get(id=self.album.id)
        images = album.get_images()
        self.assertEqual(self.image, images[0])
        self.assertEqual(len(images), 1)


class ImageModelTest(TestCase):
    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg',
                                      content=b'',
                                      content_type='image/jpeg')
        self.album = ImageAlbum.objects.create(name='MyAlbum')
        self.image = Image.objects.create(name='my img', image=self.img, album=self.album)

    def test_name_label(self):
        img = Image.objects.get(id=self.image.id)
        field_label = img._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_image_label(self):
        img = Image.objects.get(id=self.image.id)
        field_label = img._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'image')

    def test_album_label(self):
        img = Image.objects.get(id=self.image.id)
        field_label = img._meta.get_field('album').verbose_name
        self.assertEquals(field_label, 'album')

    def test_name_max_length(self):
        img = Image.objects.get(id=self.image.id)
        max_length = img._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)

    def test_str(self):
        img = Image.objects.get(id=self.image.id)
        expected = f"{img.name} | {img.album.name}"
        self.assertEquals(expected, str(img))
