# Generated by Django 4.1.2 on 2023-02-26 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0008_remove_addmessfee_sem'),
    ]

    operations = [
        migrations.AddField(
            model_name='addmessfee',
            name='feestatus',
            field=models.IntegerField(default=0),
        ),
    ]
