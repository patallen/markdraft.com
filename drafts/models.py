from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Document(models.Model):
    date_created = models.DateField('date_created', auto_now_add=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.latest_draft.title

    def _get_latest_draft(self):
        return self.drafts.order_by('-version').first()
    latest_draft = property(_get_latest_draft)


class Draft(models.Model):
    text = models.TextField(blank=False)
    version = models.IntegerField(blank=False)
    date_created = models.DateField('date_created', auto_now_add=True)
    document = models.ForeignKey(Document, related_name='drafts')

    def _get_title(self):
        return self.text.split('\n', 1)[0]
    title = property(_get_title)

    def __str__(self):
        return self.title
