# Generated by Django 4.1.2 on 2023-04-08 09:25

from django.db import migrations, models
import mycardapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0066_rename_image_account_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_bookissue',
            name='expiry_date',
            field=models.DateField(default=mycardapp.models.get_expiry),
        ),
        
    ]
