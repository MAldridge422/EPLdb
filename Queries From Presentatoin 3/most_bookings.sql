SELECT Players.name, COUNT(*) AS Bookings
FROM Players
LEFT JOIN Cards
ON Players.player_id = Cards.player_id
GROUP BY Players.player_id
ORDER BY Bookings DESC;