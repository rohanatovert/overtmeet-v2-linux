# Generated by Django 4.2.3 on 2023-11-06 14:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_callmodel_alter_attachedfile_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 6, 14, 30, 16, 856907, tzinfo=datetime.timezone.utc)),
        ),
    ]