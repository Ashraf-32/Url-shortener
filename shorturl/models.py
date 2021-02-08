from django.db import models

# Create your models here.
class Url(models.Model):
    url_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=700)
    short = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.url)