# Generated by Django 4.2.3 on 2023-11-06 15:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_alter_file_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 6, 15, 29, 22, 304561, tzinfo=datetime.timezone.utc)),
        ),
    ]
