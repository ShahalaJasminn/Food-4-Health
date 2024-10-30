# Generated by Django 5.1.2 on 2024-10-29 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dietitian', '0013_mealtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealtype',
            name='calories',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mealtype',
            name='carbohydrates',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mealtype',
            name='cholesterol',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mealtype',
            name='fat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mealtype',
            name='protein',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
