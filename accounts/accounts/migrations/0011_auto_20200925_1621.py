# Generated by Django 3.0.8 on 2020-09-25 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20200901_1501'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vespauser',
            options={'ordering': ('username',)},
        ),
    ]
