# Generated by Django 4.1.2 on 2023-03-04 10:03

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
        migrations.AlterField(
            model_name='addmessfee',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]