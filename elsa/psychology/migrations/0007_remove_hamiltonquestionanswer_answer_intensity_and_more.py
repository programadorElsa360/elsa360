# Generated by Django 4.0.5 on 2022-07-06 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psychology', '0006_alter_psycologicalquestionanswer_agreement_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hamiltonquestionanswer',
            name='answer_intensity',
        ),
        migrations.AlterField(
            model_name='hamiltonquestionanswer',
            name='answer',
            field=models.IntegerField(choices=[(0, 'Absent'), (1, 'Mild'), (2, 'Moderate'), (3, 'Grave'), (4, 'Incapacitating')], default=0),
        ),
    ]