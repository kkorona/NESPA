# Generated by Django 3.1.7 on 2021-08-16 15:31

import assignment.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0017_auto_20210814_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grademodel',
            name='grade_input',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/assignment', location='/Users/LeeJunYoung/Desktop/NESPA/data/assignment'), upload_to=assignment.models.grade_data_upload_path),
        ),
        migrations.AlterField(
            model_name='grademodel',
            name='grade_output',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/assignment', location='/Users/LeeJunYoung/Desktop/NESPA/data/assignment'), upload_to=assignment.models.grade_data_upload_path),
        ),
        migrations.AlterField(
            model_name='problemmodel',
            name='header_data',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/assignment', location='/Users/LeeJunYoung/Desktop/NESPA/data/assignment'), upload_to=assignment.models.header_data_upload_path),
        ),
        migrations.AlterField(
            model_name='problemmodel',
            name='sub_data',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/assignment', location='/Users/LeeJunYoung/Desktop/NESPA/data/assignment'), upload_to=assignment.models.sub_data_upload_path),
        ),
        migrations.AlterField(
            model_name='submissionmodel',
            name='sub_file',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/submission', location='/Users/LeeJunYoung/Desktop/NESPA/data/submission'), upload_to=assignment.models.submission_upload_path),
        ),
    ]
