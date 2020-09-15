from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0010_submissionmodel_lang'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissionmodel',
            name='prob_name',
            field=models.CharField(default='-', max_length=20),
        ),
    ]
