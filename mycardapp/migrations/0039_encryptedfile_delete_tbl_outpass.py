# Generated by Django 4.1.2 on 2023-03-22 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0038_remove_room_hostel_remove_room_name_remove_room_no_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_data', models.BinaryField()),
                ('file_name', models.CharField(max_length=255)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('key', models.BinaryField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        
    ]
