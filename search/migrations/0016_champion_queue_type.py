# Generated by Django 3.1.1 on 2021-01-22 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0015_match_queue_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='champion',
            name='Queue_type',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
    ]