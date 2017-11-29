SELECT HasPlayed.name, HasPlayed.position, HasPlayed.minutes_played
FROM
	(SELECT * FROM Players WHERE minutes_played > 0)
	AS HasPlayed
ORDER BY HasPlayed.minutes_played DESC;
