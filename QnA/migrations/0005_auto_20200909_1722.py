# Generated by Django 3.1 on 2020-09-09 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QnA', '0004_merge_20200904_1735'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date',), 'verbose_name': 'comment', 'verbose_name_plural': 'comments'},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='text',
        ),
    ]