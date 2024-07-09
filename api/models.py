import uuid
from django.db import models
from myauth.models import User
# Create your models here.

class Organisation(models.Model):
    org_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='organizations')
     
    def __str__(self) -> str:
        return self.name