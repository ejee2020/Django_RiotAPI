# Generated by Django 3.1.1 on 2021-01-26 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0033_match_champion_item6'),
    ]

    operations = [
        migrations.AddField(
            model_name='summoner',
            name='Searched',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
    ]
