# Generated by Django 4.1.2 on 2023-03-02 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0017_rename_student_id_complaintstudent_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='img',
            field=models.ImageField(default=0, upload_to='pics'),
        ),
    ]