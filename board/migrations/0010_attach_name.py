# Generated by Django 3.0.8 on 2020-10-08 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_attach'),
    ]

    operations = [
        migrations.AddField(
            model_name='attach',
            name='name',
            field=models.CharField(default='none', max_length=50),
            preserve_default=False,
        ),
    ]
