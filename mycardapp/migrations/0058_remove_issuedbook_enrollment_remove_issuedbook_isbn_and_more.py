# Generated by Django 4.1.2 on 2023-03-30 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0057_complaintbookstudent_delete_tbl_outpass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuedbook',
            name='enrollment',
        ),
        migrations.RemoveField(
            model_name='issuedbook',
            name='isbn',
        ),
       
    ]