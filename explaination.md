
# Metrics Used

## Consistency (Standard Deviation & Coefficient of Variation)

**Standard Deviation**

The standard deviation (std dev) is a metric used to measure how much individual data points differ from the mean of a set. 

**Coefficient of Variation**

The coefficient of variation measures relative variability. For example:
- A std dev of 5 for an average of 20 is a variation of .25
- A std dev of 5 for an average of 10 is a variation of .50

Because of this, coefficient variation is a better 'consistency' metric for points.

**SQL statement used**

``` sql
SELECT Player, Pos, ROUND(AVG(Pts),3) AS Avg_Pts, 
    ROUND(SQRT(AVG(Pts * Pts) - (AVG(Pts) * AVG(Pts))),3) AS Std_Dev_Pts,
    ROUND(SQRT(AVG(Pts * Pts) - (AVG(Pts) * AVG(Pts))) / AVG(Pts),3) AS Coef_Var
FROM weekly
GROUP BY Pos, Player
HAVING AVG(Pts) > 0;
```

## Projected Points

A rolling average was used to calculate projected points. 

A rolling average can be a better metric than an average over a whole season as individual and team performance tends to change throughout the season. A multiple week roll helps smooth out week-to-week variance as opposed to using only the previous week to project points.

**SQL statement used**

The first statement calculates rolling statistics for each player and notes the weeks used. The second statement then calculates the trend and projected points. The final statement filters out averages with less than 3 weeks (first two weeks) and rounds the data.

``` sql
WITH rolling AS (
    SELECT Player, Pos, Week, Pts,
        AVG(Pts) OVER (PARTITION BY Player ORDER BY Week ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_avg,
        COUNT(*) OVER (PARTITION BY Player ORDER BY Week ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS weeks_in_avg,
        LAG(Pts, 2) OVER (PARTITION BY Player ORDER BY Week) AS two_weeks_ago
    FROM weekly
),
projections AS (
    SELECT Player, Pos, Week, Pts as actual_pts, rolling_avg, weeks_in_avg,
        CASE
            WHEN weeks_in_avg >= 3 THEN (Pts - two_weeks_ago) / 2.0
            ELSE 0
        END AS trend,
        CASE
            WHEN weeks_in_avg >= 3 THEN
                rolling_avg + ((Pts - two_weeks_ago) / 2.0)
            ELSE rolling_avg
        END AS projected_pts
    FROM rolling
)
SELECT Player, Pos, Week,
    ROUND(actual_pts,2) AS actual_pts,
    ROUND(rolling_avg,2) AS rolling_avg,
    ROUND(trend,2) AS trend,
    ROUND(projected_pts,2) AS projected_pts
FROM projections
WHERE weeks_in_avg >= 3
ORDER BY Player, Week;
```
