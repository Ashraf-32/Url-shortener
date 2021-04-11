from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Url(models.Model):
    url_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=700, unique=True)
    short = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.url)