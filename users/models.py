from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    email    = models.CharField(max_length = 200, unique = True)
    password = models.CharField(max_length = 500)

    class Meta:
        db_table = 'users'
