# Generated by Django 3.1.7 on 2021-04-27 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_auto_20210426_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
