# Generated by Django 3.1.7 on 2021-07-29 16:31

import assignment.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0006_auto_20210730_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemmodel',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to=assignment.models.document_upload_path),
        ),
        migrations.AlterField(
            model_name='problemmodel',
            name='sample_data',
            field=models.FileField(blank=True, null=True, upload_to=assignment.models.sample_data_upload_path),
        ),
    ]
