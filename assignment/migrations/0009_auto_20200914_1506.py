# Generated by Django 3.0.8 on 2020-09-14 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0008_auto_20200911_2123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='problemmodel',
            options={'ordering': ('prob_id',)},
        ),
        migrations.AlterModelTable(
            name='problemmodel',
            table='problems',
        ),
    ]