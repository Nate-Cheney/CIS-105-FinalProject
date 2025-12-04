
## Metrics Used

### Consistency (Standard Deviation & Coefficient of Variation)

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


