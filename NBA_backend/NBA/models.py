from django.db import models

# Create your models here.


class PlayerIndex(models.Model):
    person_id = models.BigIntegerField(
        null=False, blank=True, primary_key=True
    )  # BigInt
    player_last_name = models.TextField(null=True, blank=True)  # Text
    player_first_name = models.TextField(null=True, blank=True)  # Text
    player_slug = models.TextField(null=True, blank=True)  # Text
    team_id = models.BigIntegerField(null=True, blank=True)  # BigInt
    team_slug = models.TextField(null=True, blank=True)  # Text
    is_defunct = models.BigIntegerField(null=True, blank=True)  # BigInt
    team_city = models.TextField(null=True, blank=True)  # Text
    team_name = models.TextField(null=True, blank=True)  # Text
    team_abbreviation = models.TextField(null=True, blank=True)  # Text
    jersey_number = models.TextField(null=True, blank=True)  # Text
    position = models.TextField(null=True, blank=True)  # Text
    height = models.TextField(null=True, blank=True)  # Text
    weight = models.TextField(null=True, blank=True)  # Text
    college = models.TextField(null=True, blank=True)  # Text
    country = models.TextField(null=True, blank=True)  # Text
    draft_year = models.FloatField(null=True, blank=True)  # Double
    draft_round = models.FloatField(null=True, blank=True)  # Double
    draft_number = models.FloatField(null=True, blank=True)  # Double
    roster_status = models.FloatField(null=True, blank=True)  # Double
    pts = models.FloatField(null=True, blank=True)  # Double
    reb = models.FloatField(null=True, blank=True)  # Double
    ast = models.FloatField(null=True, blank=True)  # Double
    stats_timeframe = models.TextField(null=True, blank=True)  # Text
    from_year = models.TextField(null=True, blank=True)  # Text
    to_year = models.TextField(null=True, blank=True)  # Text

    class Meta:
        db_table = "PlayerIndex"  # 指定資料表名稱
        verbose_name = "Player Index"
        verbose_name_plural = "Player Indices"
        managed = False

    def __str__(self):
        return f"{self.player_first_name} {self.player_last_name}"
