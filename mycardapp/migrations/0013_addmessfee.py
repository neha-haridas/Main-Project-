# Generated by Django 4.1.2 on 2023-02-26 10:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycardapp', '0012_delete_addmessfee'),
    ]

    operations = [
        migrations.CreateModel(
            name='addmessfee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feestatus', models.BooleanField(default=False)),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(9000), django.core.validators.MaxValueValidator(150000)])),
                ('date_paid', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
