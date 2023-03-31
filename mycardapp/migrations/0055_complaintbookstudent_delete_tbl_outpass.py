# Generated by Django 4.1.2 on 2023-03-30 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0054_remove_tbl_outpass_user_delete_complaintbookstudent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplaintBookStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('complaint', models.TextField(max_length=500)),
                ('complaint_reply', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycardapp.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        
    ]
