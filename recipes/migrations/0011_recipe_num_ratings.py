# Generated by Django 3.1.6 on 2021-04-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_stars'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='num_ratings',
            field=models.IntegerField(default=0),
        ),
    ]
