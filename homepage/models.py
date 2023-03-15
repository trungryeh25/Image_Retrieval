from django.db import models

# Create your models here.

class Search(models.Model):
    img = models.ImageField(upload_to = "images/upload", blank=True)
    topk = models.IntegerField(default=10)
    x = models.IntegerField(null=False, default=0)
    y = models.IntegerField(null=False, default=0)
    w = models.IntegerField(null=False, default=0)
    h = models.IntegerField(null=False, default=0)