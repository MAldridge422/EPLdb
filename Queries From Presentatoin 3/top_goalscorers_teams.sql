SELECT a.full_name AS team, COUNT(*) AS goals
FROM Teams a
INNER JOIN Goals b
ON a.team_id=b.team_id
GROUP BY a.full_name
ORDER BY goals DESC;