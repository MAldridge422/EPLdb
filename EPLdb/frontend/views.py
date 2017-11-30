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


def teams(request, team="Man Utd"):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM Teams''')
        rows = cursor.fetchall()
        all_teams = [r[1] for r in rows]
        table = None
        if team not in all_teams:
            return render(request, 'teams.html', {'table':table, 'team':team})
        cursor.execute('''
            SELECT name, position
            FROM Teams INNER JOIN Players
            ON Teams.team_id=Players.team_id
            WHERE Teams.full_name="'''+team+'''"''')
        rows = cursor.fetchall()
        table = [r for r in rows]
        cursor.execute('''
            SELECT full_name, abbrev, Managers.name as manager, Grounds.name as ground, city FROM Teams LEFT JOIN Managers ON Teams.team_id=Managers.team_id INNER JOIN Grounds ON Grounds.grounds_id=Teams.team_id AND Grounds.grounds_id=Managers.team_id WHERE Teams.full_name="'''+team+'''"''')
        rows = cursor.fetchall()
        team_obj = [r for r in rows]
        print(team_obj)
    return render(request, 'teams.html', {'team_obj':team_obj, 'team':team, 'table':table})


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
    with connection.cursor() as cursor:
        cursor.execute('''
        SELECT B.pname, B.scored, Teams.full_name
        FROM Teams
        INNER JOIN
        (
        SELECT Players.name as pname, Players.team_id as teamid, count(Players.name) as scored
        FROM Players
        INNER JOIN Goals
        ON Players.player_id=Goals.player_id
        GROUP BY Players.name
        ) B
        ON Teams.team_id = B.teamid
        ORDER BY B.scored DESC
        ''')
        rows = cursor.fetchall()
        table = [r for r in rows]
        cursor.execute('''
        SELECT B.pname, B.scored, Teams.full_name
        FROM Teams
        INNER JOIN
        (
        SELECT Players.name as pname, Players.team_id as teamid, count(Players.name) as scored
        FROM Players
        INNER JOIN Goals
        ON Players.player_id=Goals.player_id
        GROUP BY Players.name
        ) B
        ON Teams.team_id = B.teamid
        ORDER BY B.scored DESC
        LIMIT 10
        ''')
        rows = cursor.fetchall()
        top = [r for r in rows]
    return render(request, 'goals.html', {'table':table, 'top':top})

def managers(request):
    with connection.cursor() as cursor:
        cursor.execute('''
        SELECT Managers.name, Teams.full_name
        FROM Managers
            LEFT JOIN Teams
                ON Managers.team_id = Teams.team_id
        UNION ALL
        SELECT Managers.name, Teams.full_name
        FROM Teams
            LEFT JOIN Managers
                ON Managers.team_id = Teams.team_id
        WHERE Managers.team_id IS NULL
        ''')
        rows = cursor.fetchall()
        table = [r for r in rows]
    return render(request, 'managers.html', {'table':table})

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
