# Generated by Django 4.1.2 on 2023-02-26 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0007_account_sem_addmessfee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addmessfee',
            name='sem',
        ),
    ]
