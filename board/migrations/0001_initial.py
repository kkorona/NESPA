# Generated by Django 3.2.5 on 2021-08-17 10:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=50)),
                ('content', models.TextField(verbose_name='CONTENT')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='PUBLISH DATE')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='MODIFY DATE')),
                ('post_hit', models.IntegerField()),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'db_table': 'board_posts',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='PUBLISH DATE')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='MODIFY DATE')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.post')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'db_table': 'board_comments',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Attach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=100)),
                ('ext', models.CharField(max_length=10)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.post')),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
                'db_table': 'board_attachments',
            },
        ),
    ]
