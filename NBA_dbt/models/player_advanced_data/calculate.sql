SELECT
  player_id,
  player_name,
  team_abbreviation,
  age,
  gp,
  -- True Shooting Percentage
  CASE WHEN (fga + 0.44 * fta) = 0 THEN NULL
       ELSE (pts / (2 * (fga + 0.44 * fta)))
  END AS true_shooting_pct,
  -- Effective Field Goal Percentage
  CASE WHEN fga = 0 THEN NULL
       ELSE ((fgm + 0.5 * fg3m) / fga)
  END AS effective_fg_pct,
  -- Rebound Percentage (簡易版)
  CASE WHEN min = 0 THEN NULL
       ELSE (reb / (min / 48))
  END AS reb_percentage,
  -- Player Impact Estimate (簡易版)
  CASE WHEN (gp * min) = 0 THEN NULL
       ELSE ((pts + reb + ast + stl + blk - (fga - fgm) - (fta - ftm) - tov) / (gp * min))
  END AS pie,
  -- Usage Rate Estimate (簡易版)
  CASE WHEN (gp * min) = 0 THEN NULL
       ELSE ((fga + 0.44 * fta + tov) / (gp * min))
  END AS usage_rate_estimate
FROM {{ source("NBA", "player_stats_playoff")}}