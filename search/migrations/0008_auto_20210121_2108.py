# Generated by Django 3.1.1 on 2021-01-21 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0007_match_summoner'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='Champion',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='Spell1',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='Spell2',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
    ]
