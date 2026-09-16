from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE = (
        ('client','Client'),
        ('vendeur','Vendeur'),
        ('visiteur','Visiteur'),
    )

    type_user = models.CharField(max_length=20, choices=USER_TYPE, default='client')
    photo = models.ImageField(upload_to='profiles/',blank=True, null=True)
