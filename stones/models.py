import uuid
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO


class Stone(models.Model):
    draft = models.BooleanField(default=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='stones/images/stone_images', blank=True)
    found = models.BooleanField(default=False)
    found_at = models.DateTimeField(null=True, blank=True)

    finder_comment = models.OneToOneField(
        'FinderComment',
        related_name='stone',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    qr_code = models.ImageField(upload_to='stones/qrcodes/', blank=True)

    def __str__(self):
        return f"{self.title} ({self.token})"

    def get_qr_url(self):
        from django.urls import reverse
        return reverse('stone_qr', args=[self.pk])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "latitude", "longitude"],
                name="unique_stone_location"
            )
        ]

class Comment(models.Model):
    stone = models.ForeignKey(Stone, related_name="comments", on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author} - {self.text[:30]}"


class FinderComment(models.Model):
    image = models.ImageField(upload_to='stones/images/finder_images', blank=True)
    author = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author} - {self.text[:30]}"
