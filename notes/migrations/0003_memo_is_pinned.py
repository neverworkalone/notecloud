# Generated by Django 3.1.3 on 2021-02-15 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_auto_20210209_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='memo',
            name='is_pinned',
            field=models.BooleanField(default=False),
        ),
    ]