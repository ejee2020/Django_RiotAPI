# Generated by Django 3.1.1 on 2021-01-21 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0008_auto_20210121_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='Assists',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='Champ_level',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='Deaths',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='Kills',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='LargestMultiKill',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='Vision_ward',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
