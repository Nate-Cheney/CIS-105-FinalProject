
SELECT * FROM weekly;

--- Most consistent performers by position (lowest std dev of points scored) ---
SELECT Player, Pos, ROUND(AVG(Pts),3) AS Avg_Pts, 
    ROUND(SQRT(AVG(Pts * Pts) - (AVG(Pts) * AVG(Pts))),3) AS Std_Dev_Pts,
    ROUND(SQRT(AVG(Pts * Pts) - (AVG(Pts) * AVG(Pts))) / AVG(Pts),3) AS Coef_Var
FROM weekly
GROUP BY Pos, Player
HAVING AVG(Pts) > 0;



--- Rolling 3 week average with trend predicting next week's performance ---




