# Generated by Django 3.1.7 on 2021-07-29 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0005_auto_20210730_0054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submissionmodel',
            old_name='client',
            new_name='user',
        ),
    ]