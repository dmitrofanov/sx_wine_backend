from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wine_api', '0009_person_interested_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='telegram_id',
            field=models.BigIntegerField(
                verbose_name='Telegram ID',
                unique=True,
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='person',
            name='key',
            field=models.CharField(
                max_length=64,
                verbose_name='Ключ авторизации',
                unique=True,
                null=True,
                blank=True,
            ),
        ),
    ]


