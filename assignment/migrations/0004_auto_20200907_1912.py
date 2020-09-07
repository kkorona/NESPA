# Generated by Django 3.1 on 2020-09-07 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0003_auto_20200904_1631'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submissionmodel',
            old_name='client',
            new_name='client_ID',
        ),
        migrations.AddField(
            model_name='submissionmodel',
            name='client_number',
            field=models.CharField(default=202088508, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submissionmodel',
            name='code_size',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submissionmodel',
            name='exec_time',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submissionmodel',
            name='score',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='submissionmodel',
            name='result',
            field=models.CharField(max_length=40),
        ),
    ]
