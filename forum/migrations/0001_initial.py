# Generated by Django 3.1 on 2020-09-02 05:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=50)),
                ('content', models.TextField(default='', verbose_name='CONTENT')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='PUBLISH DATE')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='MODIFY DATE')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'db_table': 'forum_comments',
                'ordering': ('-mod_date',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=50)),
                ('content', models.TextField(default='', verbose_name='CONTENT')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='PUBLISH DATE')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='MODIFY DATE')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'db_table': 'forum_posts',
                'ordering': ('-mod_date',),
            },
        ),
    ]