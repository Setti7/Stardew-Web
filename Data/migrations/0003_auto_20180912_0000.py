# Generated by Django 2.0.4 on 2018-09-12 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0002_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-user'], 'verbose_name_plural': 'Profile'},
        ),
    ]
