# Generated by Django 4.1.2 on 2023-05-30 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0086_delete_tbl_outpass'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_updated',
            field=models.BooleanField(default=False),
        ),
    ]