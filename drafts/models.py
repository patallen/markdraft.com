from django.db import models
from django.contrib.auth.models import User
from hashids import Hashids


class Document(models.Model):
    hashid = models.CharField(max_length=10, db_index=True, blank=False)
    date_created = models.DateField('date_created', auto_now_add=True)
    user = models.ForeignKey(User)
    
    def __str__(self):
        return self.latest_draft.title

    def _get_latest_draft(self):
        return self.drafts.order_by('-version').first()
    latest_draft = property(_get_latest_draft)

    def update_hashid(self):
        hashids = Hashids(salt='salty', min_length=3)
        self.hashid = hashids.encode(self.id)


class Draft(models.Model):
    text = models.TextField(blank=False)
    version = models.IntegerField(blank=False)
    date_created = models.DateField('date_created', auto_now_add=True)
    document = models.ForeignKey(Document, related_name='drafts')

    def _get_title(self):
        return self.text.splitlines()[0]
    title = property(_get_title)

    def __str__(self):
        return self.title
