# Generated by Django 4.2.4 on 2023-11-01 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone', models.CharField(default='345656', max_length=100)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(to='auth.group')),
                ('permission', models.ManyToManyField(to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
