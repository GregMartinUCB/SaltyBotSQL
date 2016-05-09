SELECT T.Name,round(Avg(Bet),3),round( Sum(Wins)/COUNT(T.Name),3) AS WinRatio FROM(
SELECT name1 AS Name, bet1/(bet1+bet2) AS Bet,
	CASE 
	WHEN name1==winner THEN 1.0
	ELSE 0
	END AS Wins
FROM fights
UNION
SELECT name2 AS Name, bet2/(bet1+bet2)  AS Bet,
	CASE 
	WHEN name2==winner THEN 1.0 
	ELSE 0
	END AS Wins
FROM fights) AS T
GROUP BY T.Name;