# Generated by Django 3.1.6 on 2021-02-17 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('recipes', '0003_recipe_kcal'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.fooduser'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='images/'),
        ),
    ]
