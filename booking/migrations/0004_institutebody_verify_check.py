# Generated by Django 2.0.3 on 2018-04-02 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_remove_institutebody_registered'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutebody',
            name='verify_check',
            field=models.BooleanField(default=False),
        ),
    ]