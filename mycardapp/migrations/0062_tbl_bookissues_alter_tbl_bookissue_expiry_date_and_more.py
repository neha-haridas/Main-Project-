# Generated by Django 4.1.2 on 2023-04-01 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mycardapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0061_delete_tbl_outpass'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_BookIssues',
            fields=[
                ('issue_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_issue', models.DateField(auto_now_add=True)),
                ('expiry_date', models.DateField(default=mycardapp.models.get_expiry)),
                ('issuedstatus', models.BooleanField(default=False)),
                ('fine', models.BigIntegerField(null=True)),
                ('payment', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'), ('None', 'None')], default='Unpaid', max_length=40)),
                ('return_date', models.DateField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycardapp.book')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycardapp.category_book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='tbl_bookissue',
            name='expiry_date',
            field=models.DateField(default=mycardapp.models.get_expiry),
        ),
    ]
