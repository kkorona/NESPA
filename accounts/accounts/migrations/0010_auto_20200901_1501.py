# Generated by Django 3.0.8 on 2020-09-01 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_merge_20200901_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vespauser',
            name='email',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='vespauser',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
