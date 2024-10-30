# Generated by Django 5.1.2 on 2024-10-23 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_account', '0004_alter_user_profile_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'MALE'), ('female', 'FEMALE'), ('other', 'PREFER NOT TO SAY')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]