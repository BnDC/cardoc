from django.db   import models

from core.models import TimeStampModel

class Trim(TimeStampModel):
    trim_id    = models.PositiveIntegerField()
    front_tire = models.ForeignKey('Tire', on_delete = models.CASCADE, related_name = 'trim_front_tire')
    back_tire  = models.ForeignKey('Tire', on_delete = models.CASCADE, related_name = 'trim_back_tire')

    class Meta:
        db_table = 'trims'

class Tire(TimeStampModel):
    width         = models.PositiveIntegerField()
    asepect_ratio = models.PositiveIntegerField()
    size          = models.PositiveIntegerField()

    class Meta:
        db_table = 'tires'