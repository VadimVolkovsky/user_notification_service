# Generated by Django 4.2.5 on 2024-08-15 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_remove_notification_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allowed_email', models.BooleanField(default=True)),
                ('allowed_push', models.BooleanField(default=True)),
                ('time_zone', models.CharField(max_length=10)),
            ],
        ),
    ]
