# Generated by Django 3.1 on 2020-09-07 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',), 'verbose_name': 'post', 'verbose_name_plural': 'posts'},
        ),
    ]
