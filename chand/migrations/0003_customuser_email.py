# Generated by Django 5.1.6 on 2025-02-19 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chand', '0002_auto_20250219_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default='example@gmail.com', max_length=254, unique=True),
        ),
    ]
