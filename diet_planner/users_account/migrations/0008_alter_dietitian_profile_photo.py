# Generated by Django 5.1.2 on 2024-10-25 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_account', '0007_alter_accounts_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dietitian_profile',
            name='photo',
            field=models.ImageField(default='assets/profile.png', upload_to='dietitian_photos'),
        ),
    ]