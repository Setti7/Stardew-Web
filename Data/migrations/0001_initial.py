# Generated by Django 2.0.4 on 2018-09-25 17:36

import Data.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profile',
                'ordering': ['-user'],
            },
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=Data.models.user_directory_path)),
                ('score', models.IntegerField(default=0)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Data',
                'ordering': ['-score'],
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=20, unique=True)),
                ('log', models.TextField(max_length=500)),
                ('date', models.DateField()),
                ('critical', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Version',
                'verbose_name_plural': 'Version',
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='userdata',
            name='version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Data.Version'),
        ),
    ]
