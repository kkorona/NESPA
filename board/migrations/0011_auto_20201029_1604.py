# Generated by Django 3.1 on 2020-10-29 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_attach_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='CONTENT'),
        ),
    ]