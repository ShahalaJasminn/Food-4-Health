# Generated by Django 5.1.2 on 2024-10-27 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dietitian', '0002_availability_day_alter_availability_dietitian_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='day',
            field=models.TextField(blank=True, default=''),
        ),
    ]
