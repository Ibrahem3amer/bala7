from django.db import models

# Create your models here.
class University(models.Model):
    uni_type = models.CharField(max_length=200)
    bio = models.CharField(max_length=200)