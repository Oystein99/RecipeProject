# Generated by Django 3.1.6 on 2021-04-17 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210223_0044'),
        ('recipes', '0011_recipe_num_ratings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.fooduser')),
            ],
        ),
        migrations.AddConstraint(
            model_name='ratings',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_rating'),
        ),
    ]