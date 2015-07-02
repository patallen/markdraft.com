from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Draft(models.Model):
    current_title = models.CharField(max_length=240)
    current_version = models.IntegerField()
    date_created = models.DateField('date_created', auto_now_add=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.current_title
