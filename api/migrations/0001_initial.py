# Generated by Django 2.0.4 on 2018-07-10 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Data', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=1000)),
                ('contact', models.EmailField(blank=True, max_length=254, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('version', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Data.Version')),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]
