# Generated by Django 2.0.3 on 2018-04-02 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_institutebody_verify_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutebody',
            name='registered',
            field=models.BooleanField(default=False),
        ),
    ]
