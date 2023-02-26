# Generated by Django 4.1.2 on 2023-02-24 05:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mycardapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('contact', models.BigIntegerField(default=0)),
                ('address', models.CharField(default='', max_length=50)),
                ('pin', models.BigIntegerField(default=0)),
                ('regno', models.BigIntegerField(default=0, unique=True)),
                ('dpmnt', models.CharField(default='', max_length=50)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_user', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_libry', models.BooleanField(default=False)),
                ('is_warden', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Category_Book',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssuedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment', models.CharField(max_length=30)),
                ('isbn', models.CharField(max_length=30)),
                ('issuedate', models.DateField(auto_now=True)),
                ('expirydate', models.DateField(default=mycardapp.models.get_expiry)),
            ],
        ),
        migrations.CreateModel(
            name='librarian',
            fields=[
                ('libid', models.AutoField(primary_key=True, serialize=False)),
                ('First_name', models.CharField(default='', max_length=50)),
                ('Last_name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('Phone_number', models.BigIntegerField(default=0)),
                ('is_libr', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=100)),
                ('descrip', models.CharField(max_length=100)),
                ('pdf', models.FileField(upload_to='media')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mycardapp.category')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_name', models.CharField(max_length=100)),
                ('book_quantity', models.BigIntegerField(default=0)),
                ('book_price', models.BigIntegerField(default=0)),
                ('book_author', models.CharField(max_length=50)),
                ('book_year', models.BigIntegerField(default=0)),
                ('book_language', models.CharField(max_length=50)),
                ('book_publisher', models.CharField(max_length=100)),
                ('book_status', models.BooleanField(default=True)),
                ('book_desc', models.TextField()),
                ('isbn', models.PositiveIntegerField(default=0)),
                ('img', models.ImageField(upload_to='pics')),
                ('img2', models.ImageField(default=0, upload_to='pics')),
                ('book_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mycardapp.category_book', verbose_name='Category_Book')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
