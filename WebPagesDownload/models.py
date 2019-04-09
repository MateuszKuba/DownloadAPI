from django.db import models


def image_path(instance, filename):
    return 'images/{}'.format(
        filename
    )

def text_path(instance, filename):
    return 'texts/{}'.format(
        filename
    )

PENDING = 0
DONE = 1
FAILED = -1
STATUS_CHOICES = (
    (PENDING, 'Pending'),
    (DONE, 'Done'),
    (FAILED,'Failed')
)


class Download(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()


class WebImage(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.ImageField(upload_to=image_path)
    download = models.ForeignKey(Download, on_delete=models.CASCADE, related_name='webimage')


class WebText(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.FileField(upload_to=text_path)
    download = models.ForeignKey(Download, on_delete=models.CASCADE, related_name='webtext')


