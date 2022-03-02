# Generated by Django 3.1.7 on 2021-04-27 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0018_auto_20210427_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='numKeywords',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='word',
            name='docFrequency',
            field=models.FloatField(default=1),
        ),
    ]