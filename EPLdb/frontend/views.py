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


def teams(request, team="Manchester United"):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM TEAMS''')
        rows = cursor.fetchall()
        all_teams = [r[1] for r in rows]
        table = None
        if team not in all_teams:
            return render(request, 'teams.html', {'table':table, 'team':team})
        # need to finish the function here
    return render(request, 'teams.html', {'team':team})


def positions(request, pos="Defender"):
    positions = ["GoalKeeper", "Defender", "Midfielder", "Forward"]
    table = None
    if pos not in positions:
        return render(request, 'positions.html', {'table': table})
    with connection.cursor() as cursor:
        cursor.execute('''
            DROP VIEW IF EXISTS '''+pos
        )
        cursor.execute('''
            CREATE VIEW ''' + pos + ''' AS
            SELECT *
            FROM Players
            WHERE position="''' + pos + '''"
        ''')
        cursor.execute('''SELECT name, full_name, minutes_played, assists, saves FROM '''+pos+''' NATURAL JOIN Teams''')
        rows = cursor.fetchall()
        table = [r for r in rows]
    return render(request, 'positions.html', {'table': table, 'pos':pos})


def bookings(request, col='yellow'):
    if col=='yellow':
        col = 0
    else:
        col = 1
    with connection.cursor() as cursor:
        cursor.execute('''
        SELECT name, count(name)
        FROM Cards
        INNER JOIN Players
        ON Cards.player_id=Players.player_id
        WHERE is_red='''+str(col)+'''
        GROUP BY name''') 
        rows = cursor.fetchall()
        table = [r for r in rows]
    if col==0:
        col='Yellow'
    else:
        col='Red'
    return render(request, 'bookings.html', {'table':table, 'col':col})


def goals(request):
    return render(request, 'goals.html')


def raw_data(request, tname):
    theaders = []
    table = []
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info("+tname+")")
        rows = cursor.fetchall()
        theaders = [r[1] for r in rows]
        cursor.execute('''
            SELECT * FROM '''+tname
        )
        rows = cursor.fetchall()
        table = [r for r in rows]
    return render(request, 'raw_data.html', {'table':table, 'tname':tname, 'theaders':theaders})
