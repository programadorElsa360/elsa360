# Generated by Django 4.0.5 on 2022-07-06 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_training_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='training_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='training_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]