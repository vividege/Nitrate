# Generated by Django 2.2.7 on 2020-01-31 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcms.core.contrib.auth', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            'CREATE INDEX idx_user_email ON auth_user (email)'
        )
    ]