# Generated by Django 3.0.8 on 2020-09-23 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20200922_1220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date',), 'verbose_name': 'comment', 'verbose_name_plural': 'comments'},
        ),
    ]
