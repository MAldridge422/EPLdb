from django.shortcuts import render
from django.db import connection

def index(request):
    table = []
    with connection.cursor() as cursor:
        # league table
        cursor.execute('''
            SELECT full_name, played, wins, draws,
                (played-wins-draws) as losses,gf,ga,(gf-ga) AS gd,
                (wins*3 + draws) as points
            FROM
            (SELECT full_name, count(full_name) AS played
            FROM Fixtures
            INNER JOIN Teams
            ON away_team=team_id OR home_team=team_id
            GROUP BY full_name) PLAYED

            NATURAL JOIN

            (SELECT full_name, count(winner_id) AS wins
            FROM Fixtures
            INNER JOIN Teams
            ON winner_id=team_id
            GROUP BY full_name) WINS

            NATURAL JOIN

            (SELECT full_name, count(full_name) AS draws
            FROM Fixtures
            INNER JOIN Teams
            ON winner_id IS NULL AND
                (away_team=team_id OR home_team=team_id)
            GROUP BY full_name) DRAWS

            NATURAL JOIN

            (SELECT full_name, (hgf+agf) as gf
              FROM
              (SELECT full_name, sum(home_goals) AS hgf
              FROM Fixtures INNER JOIN Teams
              WHERE home_team=team_id
              GROUP BY full_name) HGF
              NATURAL JOIN
              (SELECT full_name, sum(away_goals) AS agf
              FROM Fixtures INNER JOIN Teams
              WHERE away_team=team_id
              GROUP BY full_name) AGF
              ) GF

            NATURAL JOIN

            (SELECT full_name, (hga+aga) as ga
              FROM
              (SELECT full_name, sum(home_goals) AS hga
              FROM Fixtures INNER JOIN Teams
              WHERE away_team=team_id
              GROUP BY full_name) HGA
              NATURAL JOIN
              (SELECT full_name, sum(away_goals) AS aga
              FROM Fixtures INNER JOIN Teams
              WHERE home_team=team_id
              GROUP BY full_name) AGA
              ) GA
              ORDER BY points DESC, gd DESC
        ''')
        rows = cursor.fetchall()
        table = [r for r in rows]
    return render(request, 'index.html', {'table': table})

def teams(request):
    return render(request, 'teams.html',)

def positions(request):
    return render(request, 'positions.html',)

def bookings(request):
    return render(request, 'bookings.html',)

def goals(request):
    return render(request, 'goals.html',)

def raw_data(request):
    return render(request, 'raw_data.html',)
