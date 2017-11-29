SELECT abbrev, full_name, Managers.name as manager, Grounds.name as ground, city
FROM Teams
  LEFT JOIN Managers
    ON Teams.team_id = Managers.team_id
  INNER JOIN Grounds
  ON Grounds.grounds_id = Teams.team_id
  AND Grounds.grounds_id = Managers.team_id;
