SELECT a.name AS player, COUNT(*) AS goals
FROM Players a
INNER JOIN Goals b
ON a.player_id=b.player_id
GROUP BY a.name
ORDER BY goals DESC;
