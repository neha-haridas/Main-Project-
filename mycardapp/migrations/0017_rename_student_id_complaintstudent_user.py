# Generated by Django 4.1.2 on 2023-02-27 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0016_complaintstudent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complaintstudent',
            old_name='student_id',
            new_name='user',
        ),
    ]