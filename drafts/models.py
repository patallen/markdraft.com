from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Document(models.Model):
    latest_version = models.IntegerField()
    date_created = models.DateField('date_created', auto_now_add=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return '{} {}'.format(self.user.username, str(self.latest_version))


class Draft(models.Model):
    text = models.TextField(blank=False)
    version = models.IntegerField(blank=False)
    date_created = models.DateField('date_created', auto_now_add=True)
    document = models.ForeignKey(Document)

    def __str__(self):
        return self.text.split('\n', 1)[0]
