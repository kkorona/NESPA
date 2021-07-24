# Generated by Django 3.1.7 on 2021-07-24 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QnA', '0009_attach'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='retweet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='QnA.comment'),
        ),
    ]
