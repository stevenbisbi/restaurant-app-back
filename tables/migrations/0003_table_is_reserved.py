# Generated by Django 5.1.7 on 2025-06-02 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0002_alter_table_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='is_reserved',
            field=models.BooleanField(default=False),
        ),
    ]
