# Generated by Django 3.2.7 on 2021-11-28 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tires', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tire',
            old_name='asepect_ratio',
            new_name='aspect_ratio',
        ),
    ]
