# Generated by Django 3.1.1 on 2021-01-25 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0023_auto_20210125_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='Main',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='search.match_champion'),
        ),
    ]
