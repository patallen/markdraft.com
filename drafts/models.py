from django.db import models

# Create your models here.


class Draft(models.Model):
    current_title = models.CharField(max_length=240)
    current_version = models.IntegerField()
    date_created = models.DateField('date_created', auto_now_add=True)

    def __str__(self):
        return self.current_title
