# Generated by Django 4.0.5 on 2022-07-11 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_plans', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cyclingplan',
            name='cycling_training_intensity',
            field=models.IntegerField(choices=[(4, 'Very light'), (6, 'Light'), (8, 'Moderate'), (10, 'Strong')], default=6),
        ),
    ]
