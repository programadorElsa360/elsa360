# Generated by Django 4.0.5 on 2022-07-06 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('psychology', '0003_psychologicaltraining'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PsychologicalTraining',
            new_name='PsychologicalTechnique',
        ),
    ]
