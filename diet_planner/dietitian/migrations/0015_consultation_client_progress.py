# Generated by Django 5.1.2 on 2024-10-30 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dietitian', '0014_mealtype_calories_mealtype_carbohydrates_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='client_progress',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
