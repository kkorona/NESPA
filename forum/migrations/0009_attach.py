from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_auto_20200923_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=100)),
                ('ext', models.CharField(max_length=10)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Post')),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
                'db_table': 'forum_attachments',
            },
        ),
    ]
