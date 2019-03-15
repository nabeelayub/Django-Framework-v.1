from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.urls import reverse


class User(AbstractUser):
   images=models.ImageField(default='default.jpg')

   def get_absolute_url(self):
      return reverse('login')






