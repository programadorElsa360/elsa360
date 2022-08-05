# Generated by Django 4.0.5 on 2022-07-12 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_training_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.IntegerField(default=26),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='height',
            field=models.FloatField(default=173, help_text='Customer height in centimeters'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='weight',
            field=models.FloatField(default=75.5, help_text='Customer weight in kilograms'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='weight_goal',
            field=models.FloatField(default=70.0),
            preserve_default=False,
        ),
    ]