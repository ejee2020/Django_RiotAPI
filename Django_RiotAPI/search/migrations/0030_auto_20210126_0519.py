# Generated by Django 3.1.1 on 2021-01-26 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0029_match_champion_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='Summoners',
        ),
        migrations.AddField(
            model_name='match',
            name='Team1',
            field=models.ManyToManyField(related_name='team1', to='search.Match_Champion'),
        ),
        migrations.AddField(
            model_name='match',
            name='Team2',
            field=models.ManyToManyField(related_name='team2', to='search.Match_Champion'),
        ),
    ]
