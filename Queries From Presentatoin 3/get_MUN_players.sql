SELECT a.name, b.full_name
FROM Players a
INNER JOIN Teams b
ON a.team_id=b.team_id
WHERE b.abbrev='MUN';