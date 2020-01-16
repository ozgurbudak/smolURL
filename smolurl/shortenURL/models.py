from django.db import models

# Create your models here.
class URL(models.Model):
    address= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
