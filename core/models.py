from django.db import models

class TimeStampModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    class Meta:
        abstract = True
