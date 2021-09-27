from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Summoner(models.Model):
    Name = models.CharField(max_length=200, db_index=True)
    Searched = models.CharField(max_length=200, db_index=True, default="False")
    Most_recent = models.PositiveIntegerField(default=0)
    Num_played = models.PositiveIntegerField(default=0)
    Adc_played = models.PositiveIntegerField(default=0)
    Top_played = models.PositiveIntegerField(default=0)
    Sup_played = models.PositiveIntegerField(default=0)
    Mid_played = models.PositiveIntegerField(default=0)
    Jun_played = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.Name


class Champion(models.Model):
    Name = models.CharField(max_length=200, db_index=True)
    Summoner = models.ForeignKey(
        Summoner, on_delete=models.CASCADE, null=True)
    Queue_type = models.CharField(max_length=200, db_index=True, null=True)
    Img_link = models.CharField(max_length=200, db_index=True)
    Num_played = models.PositiveIntegerField(default=0)
    Num_won = models.PositiveIntegerField(default=0)
    Kills = models.PositiveIntegerField(default=0)
    Assists = models.PositiveIntegerField(default=0)
    Deaths = models.PositiveIntegerField(default=0)
    CS = models.PositiveIntegerField(default=0)
    Mins_played = models.PositiveIntegerField(default=0)
    Damage_dealt = models.PositiveIntegerField(default=0)
    Gold = models.PositiveIntegerField(default=0)
    KDA = models.PositiveIntegerField(default=0)
    Kill_pg = models.PositiveIntegerField(default=0)
    Death_pg = models.PositiveIntegerField(default=0)
    Assist_pg = models.PositiveIntegerField(default=0)
    Winrate = models.PositiveIntegerField(default=0)
    Dpm = models.PositiveIntegerField(default=0)
    Gpm = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-Num_played']

    def __str__(self):
        return self.Name

    def change(self, data):
        self.Num_played += 1
        if data['stats']['win'] == True:
            self.Num_won += 1
        self.Kills += data['stats']['kills']
        self.Deaths += data['stats']['deaths']
        self.Assists += data['stats']['assists']
        self.CS += data['stats']['totalMinionsKilled']
        self.Damage_dealt += data['stats']['totalDamageDealtToChampions']
        self.Gold += data['stats']['goldEarned']
        self.save()

    def finish(self):
        if self.Deaths == 0:
            self.Kda = self.Kills + self.Assists
        else:
            self.Kda = round((self.Kills + self.Assists) / self.Deaths, 2)

        self.Kill_pg = round(self.Kills / self.Num_played, 2)
        self.Death_pg = round(self.Deaths / self.Num_played, 2)
        self.Assist_pg = round(self.Assists / self.Num_played, 2)
        self.Winrate = round(100 * self.Num_won / self.Num_played)
        self.Dpm = round(self.Damage_dealt / self.Mins_played, 2)
        self.Gpm = round(self.Gold / self.Mins_played, 2)
        self.save()


class Match_Champion(models.Model):
    Damage_dealt = Position = models.PositiveIntegerField(default=0)
    Summoner_name = models.CharField(max_length=200, db_index=True, null=True)
    Win = models.CharField(max_length=200, db_index=True, null=True)
    Role = models.CharField(max_length=200, db_index=True, null=True)
    Position = models.PositiveIntegerField(default=0)
    Match_id = models.PositiveIntegerField(default=0)
    Min_played = models.PositiveIntegerField(default=0)
    Sec_played = models.PositiveIntegerField(default=0)
    Queue_type = models.CharField(max_length=200, db_index=True, null=True)
    Champion = models.CharField(max_length=200, db_index=True, null=True)
    Champion_link = models.CharField(max_length=200, db_index=True, null=True)
    Spell1 = models.CharField(max_length=200, db_index=True, null=True)
    Spell2 = models.CharField(max_length=200, db_index=True, null=True)
    Item0 = models.CharField(max_length=200, db_index=True, null=True)
    Item1 = models.CharField(max_length=200, db_index=True, null=True)
    Item2 = models.CharField(max_length=200, db_index=True, null=True)
    Item3 = models.CharField(max_length=200, db_index=True, null=True)
    Item4 = models.CharField(max_length=200, db_index=True, null=True)
    Item5 = models.CharField(max_length=200, db_index=True, null=True)
    Item6 = models.CharField(max_length=200, db_index=True, null=True)
    Perk0 = models.CharField(max_length=200, db_index=True, null=True)
    Perk1 = models.CharField(max_length=200, db_index=True, null=True)
    Perk2 = models.CharField(max_length=200, db_index=True, null=True)
    Perk3 = models.CharField(max_length=200, db_index=True, null=True)
    Perk4 = models.CharField(max_length=200, db_index=True, null=True)
    Perk5 = models.CharField(max_length=200, db_index=True, null=True)
    Kills = models.PositiveIntegerField(default=0)
    Deaths = models.PositiveIntegerField(default=0)
    Assists = models.PositiveIntegerField(default=0)
    Kda = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    LargestMultiKill = models.CharField(
        max_length=200, db_index=True, null=True)
    Champ_level = models.PositiveIntegerField(default=0)
    Vision_ward = models.PositiveIntegerField(default=0)
    Summoner = models.ForeignKey(
        Summoner, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.Match_id)

    def finish(self):
        if self.Deaths == 0:
            self.Kda = self.Kills + self.Assists
            self.save()
        else:
            self.Kda = round((self.Kills + self.Assists) / self.Deaths, 2)
            self.save()


class Match(models.Model):
    Match_id = models.PositiveIntegerField(default=0)
    Min_played = models.PositiveIntegerField(default=0)
    Sec_played = models.PositiveIntegerField(default=0)
    Queue_type = models.CharField(max_length=200, db_index=True, null=True)
    Result = models.CharField(max_length=200, db_index=True, null=True)
    Team1 = models.ManyToManyField(Match_Champion, related_name="team1")
    Team2 = models.ManyToManyField(Match_Champion, related_name="team2")
    Main = models.ForeignKey(
        Match_Champion, on_delete=models.CASCADE, null=True)
    Summoner = models.ForeignKey(
        Summoner, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.Match_id)
