
SELECT * FROM weekly;

--- Most consistent performers by position (lowest std dev of points scored) ---
SELECT Player, Pos, ROUND(AVG(Pts),3) AS Avg_Pts, 
    ROUND(SQRT(AVG(Pts * Pts) - (AVG(Pts) * AVG(Pts))),3) AS Std_Dev_Pts,
    ROUND(SQRT(AVG(Pts * Pts) - (AVG(Pts) * AVG(Pts))) / AVG(Pts),3) AS Coef_Var
FROM weekly
GROUP BY Pos, Player
HAVING AVG(Pts) > 0;


--- Rolling 3 week average with trend predicting next week's performance ---
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
