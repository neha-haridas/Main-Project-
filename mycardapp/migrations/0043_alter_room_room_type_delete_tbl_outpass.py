# Generated by Django 4.1.2 on 2023-03-22 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0042_delete_encryptedfile_delete_tbl_outpass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('S', 'Single Room'), ('D', 'Double Room'), ('T', 'Triple Room'), ('P', 'Reserved for Research Scholars'), ('B', 'Both Single and Double Occupancy')], default=None, max_length=1),
        ),
       
    ]
