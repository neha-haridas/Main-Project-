# Generated by Django 4.1.2 on 2023-02-24 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0003_alter_tbl_outpass_parents_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_outpass',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('None', 'None')], default=0, max_length=100),
        ),
    ]
