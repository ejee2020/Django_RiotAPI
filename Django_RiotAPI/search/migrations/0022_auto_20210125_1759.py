# Generated by Django 3.1.1 on 2021-01-25 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0021_auto_20210125_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='Summoners',
            field=models.ManyToManyField(related_name='summoner', to='search.Match_Champion'),
        ),
    ]