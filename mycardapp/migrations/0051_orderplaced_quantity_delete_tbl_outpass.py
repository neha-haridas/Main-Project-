# Generated by Django 4.1.2 on 2023-03-28 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0050_room_user_delete_tbl_outpass'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        
    ]
