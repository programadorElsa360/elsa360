# Generated by Django 4.0.5 on 2022-07-05 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='membership_purchased',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='memberships.membership'),
        ),
    ]
