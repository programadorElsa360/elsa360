# Generated by Django 4.0.5 on 2022-07-06 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psychology', '0005_hamiltonquestion_hamiltonquestionanswer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psycologicalquestionanswer',
            name='agreement_answer',
            field=models.CharField(blank=True, choices=[('TD', 'Total disagreement'), ('MD', 'Much disagreement'), ('SD', 'Some disagreement'), ('SA', 'Some agreement'), ('MA', 'Much agreement'), ('TA', 'Total agreement')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='psycologicalquestionanswer',
            name='qualificative_answer',
            field=models.IntegerField(blank=True, choices=[(0, 'Very good'), (1, 'Good'), (2, 'Normal'), (3, 'Regular'), (4, 'Bad')], null=True),
        ),
    ]
