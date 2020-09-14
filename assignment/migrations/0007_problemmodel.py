# Generated by Django 3.1 on 2020-09-11 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0006_auto_20200908_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prob_id', models.CharField(max_length=20)),
                ('starts_at', models.DateTimeField()),
                ('ends_at', models.DateTimeField()),
                ('size_limit', models.IntegerField()),
                ('time_limit', models.FloatField()),
            ],
        ),
    ]