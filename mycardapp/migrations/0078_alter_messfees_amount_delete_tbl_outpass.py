# Generated by Django 4.1.2 on 2023-04-22 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0077_alter_messfees_payment_id_delete_tbl_outpass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messfees',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]