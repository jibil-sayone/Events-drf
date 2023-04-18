from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.

CATEGORY_CHOICES = (("Music", 'Music'), ('Sports', 'Sports'))

class Events(models.Model):

    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    published = models.BooleanField(default=False)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='images', null=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

class Comments(models.Model):

    comment = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Events, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


