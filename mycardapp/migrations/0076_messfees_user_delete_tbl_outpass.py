# Generated by Django 4.1.2 on 2023-04-14 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0075_messfees_delete_tbl_outpass'),
    ]

    operations = [
        migrations.AddField(
            model_name='messfees',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        
    ]