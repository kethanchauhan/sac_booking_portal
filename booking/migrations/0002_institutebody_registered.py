# Generated by Django 2.0.3 on 2018-03-27 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutebody',
            name='registered',
            field=models.BooleanField(default=False),
        ),
    ]
