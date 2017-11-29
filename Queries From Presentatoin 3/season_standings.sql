--
-- Matches Played
--
/*SELECT abbrev,
    (home_wins + away_wins) as wins,
    (home_wins + away_wins)*3 as points,
    goals_for, goals_against, goal_differential
    FROM
(*/
SELECT * FROM
(
SELECT count(*) AS matched_played, Teams.abbrev
FROM Fixtures
INNER JOIN Teams
ON Fixtures.home_team=Teams.team_id OR Fixtures.away_team=Teams.team_id
GROUP BY Teams.team_id
) MP

NATURAL JOIN

--
-- Home Wins
--
(
SELECT count(winner_id) AS home_wins, Teams.abbrev
FROM Fixtures
INNER JOIN Teams
ON Fixtures.home_team=Teams.team_id
GROUP BY Teams.team_id
) HW

NATURAL JOIN

--
-- Away Wins
--
(
SELECT count(winner_id) AS away_wins, Teams.abbrev
FROM Fixtures
INNER JOIN Teams
ON Fixtures.away_team=Teams.team_id
GROUP BY Teams.team_id
) AW
;


SELECT abbrev, goals_for, goals_against, (goals_for - goals_against) AS goal_differential FROM
(
SELECT Teams.abbrev, COUNT(*) AS goals_for
FROM Teams
INNER JOIN Goals
ON Teams.team_id=Goals.team_id
GROUP BY Teams.abbrev
) GF

NATURAL JOIN

(
SELECT (GA_home + GA_away) AS goals_against, abbrev FROM
(SELECT gah.GA_home, gaa.GA_away, team_id
FROM (
	--
	-- Goals Against (Home)
	--
	(SELECT COUNT(Goals.goal_id) AS GA_home, Fixtures.home_team AS team_id
	FROM Goals
	INNER JOIN Fixtures
	ON Fixtures.fixture_id=Goals.fixture_id
	WHERE Fixtures.away_team=Goals.team_id
	GROUP BY Fixtures.home_team) gah

	NATURAL JOIN

	--
	-- Goals Against (Away)
	--
	(SELECT COUNT(Goals.goal_id) AS GA_away, Fixtures.away_team AS team_id
	FROM Goals
	INNER JOIN Fixtures
	ON Fixtures.fixture_id=Goals.fixture_id
	WHERE Fixtures.home_team=Goals.team_id
	GROUP BY Fixtures.away_team) gaa
	)
GROUP BY team_id
) GA2

NATURAL JOIN

Teams) GA
;
/*ORDER BY points DESC, goal_differential DESC
;*/
