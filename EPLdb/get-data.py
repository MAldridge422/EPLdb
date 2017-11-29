import json
import urllib.request
import sqlite3

'''setup db connection'''
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

'''This func traverses a JSON file, outputting a user-readable tree'''
def key_tree(data, indents, is_list):
	for k in data.keys():
		if is_list:
			print(" "*2*indents + "*" + k)
		else:
			print(" "*2*indents + k)
		if(isinstance(data[k], dict)):
			key_tree(data[k], indents+1, False)
		elif(isinstance(data[k], list)):
			if(len(data[k]) > 0 and isinstance(data[k][0], dict)):
				key_tree(data[k][0], indents+1, True)

'''Generates Teams table'''
def teams():
    cur.execute('''
        DROP TABLE IF EXISTS `Teams`;
    ''')
    cur.execute('''
        CREATE TABLE `Teams` (
            `team_id` int(11) NOT NULL,
            `full_name` varchar(64) NOT NULL,
            `nickname` varchar(64) DEFAULT NULL,
            `abbrev` char(3) NOT NULL,
            PRIMARY KEY (`team_id`)
        )
    ''')
    conn.commit()
    nicknames = {
        'ARS':'Gunners',
        'BOU':'Poppers',
        'BHA':'Seagulls',
        'BUR':'Clarets',
        'CHE':'Blues',
        'CRY':'Eagles',
        'EVE':'Toffees',
        'HUD':'Terriers',
        'LEI':'Foxes',
	    'LIV':'Reds',
	    'MCI':'Citizens',
	    'MUN':'Red Devils',
	    'NEW':'Magpies',
	    'SOU':'Saints',
	    'STK':'Potters',
	    'SWA':'Swans',
	    'TOT':'Spurs',
	    'WAT':'Hornets',
	    'WBA':'Baggies',
	    'WHU':'Hammers',
	}
    teams = data['teams']
    for t in teams:
        team_id = int(t['id'])
        name = t['name']
        code = int(t['code'])
        abbrev = t['short_name']
        nickname = nicknames[abbrev]
        cur.execute('''
            INSERT INTO Teams (team_id, full_name, nickname, abbrev)
            VALUES
            (?, ?, ?, ?)''',
            (team_id, name, nickname, abbrev)
        )
        conn.commit()

'''Generates Players table'''
def players():
    cur.execute('''
        DROP TABLE IF EXISTS `Players`;
    ''')
    cur.execute('''
        CREATE TABLE `Players` (
            `player_id` int(11) NOT NULL,
            `name` varchar(64) NOT NULL,
            `position` varchar(16) NOT NULL,
            `minutes_played` int(11) DEFAULT NULL,
            `assists` int(11) DEFAULT NULL,
            `saves` int(11) DEFAULT NULL,
            `team_id` int(11) DEFAULT NULL,
            PRIMARY KEY (`player_id`),
            CONSTRAINT `plays for` FOREIGN KEY (`team_id`) REFERENCES `Teams` (`team_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
        )
    ''')
    conn.commit()
    positions = {
	   1:"GoalKeeper",
	   2:"Defender",
	   3:"Midfielder",
	   4:"Forward"
    }
    players = data['elements']
    for p in players:
        player_id = int(p['id'])
        name = p['web_name']
        position = positions[p['element_type']]
        minutes_played = int(p['minutes'])
        assists = int(p['assists'])
        saves = int(p['saves'])
        team_id = p['team']
        cur.execute('''
            INSERT INTO Players (player_id, name, position, minutes_played, assists, saves, team_id)
            VALUES
            (?, ?, ?, ?, ?, ?, ?)''',
            (player_id, name, position, minutes_played, assists, saves, team_id)
        )
        conn.commit()
    

'''Generates Fixtures table'''
def fixtures():
    cur.execute('''
        DROP TABLE IF EXISTS `Fixtures`;
    ''')
    cur.execute('''
        CREATE TABLE `Fixtures` (
          `fixture_id` int(11) NOT NULL,
          `home_goals` int(11) DEFAULT NULL,
          `away_goals` int(11) DEFAULT NULL,
          `home_team` int(11) DEFAULT NULL,
          `away_team` int(11) DEFAULT NULL,
          `winner_id` int(11) DEFAULT NULL,
          `referee_id` int(11) DEFAULT NULL,
          PRIMARY KEY (`fixture_id`),
          CONSTRAINT `away_team` FOREIGN KEY (`away_team`) REFERENCES `Teams` (`team_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `home_team` FOREIGN KEY (`home_team`) REFERENCES `Teams` (`team_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `referee_id` FOREIGN KEY (`referee_id`) REFERENCES `Referees` (`ref_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `winner_id` FOREIGN KEY (`winner_id`) REFERENCES `Teams` (`team_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
        )
    ''')
    conn.commit()
    # TODO: generate this data


'''Generates Cards table'''
def cards():
    cur.execute('''
        DROP TABLE IF EXISTS `Cards`;
    ''')
    cur.execute('''
        CREATE TABLE `Cards` (
          `card_id` int(11) NOT NULL,
          `is_red` tinyint(4) DEFAULT NULL,
          `fixture_id` int(11) DEFAULT NULL,
          `player_id` int(11) DEFAULT NULL,
          PRIMARY KEY (`card_id`),
          CONSTRAINT `fixture_in` FOREIGN KEY (`fixture_id`) REFERENCES `Fixtures` (`fixture_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `player_to` FOREIGN KEY (`player_id`) REFERENCES `Players` (`player_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
        )
    ''')
    conn.commit()
    # TODO: generate this data


'''Generates Goals table'''
def goals():
    cur.execute('''
        DROP TABLE IF EXISTS `Goals`;
    ''')
    cur.execute('''
        CREATE TABLE `Goals` (
          `goal_id` int(11) NOT NULL,
          `player_id` int(11) DEFAULT NULL,
          `team_id` int(11) DEFAULT NULL,
          `fixture_id` int(11) DEFAULT NULL,
          PRIMARY KEY (`goal_id`),
          CONSTRAINT `fixture` FOREIGN KEY (`fixture_id`) REFERENCES `Fixtures` (`fixture_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `scorer` FOREIGN KEY (`player_id`) REFERENCES `Players` (`player_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `team_scorer` FOREIGN KEY (`team_id`) REFERENCES `Teams` (`team_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
        )
    ''')
    conn.commit()
    # TODO: generate this data


'''Generates Managers table'''
def managers():
    cur.execute('''
      DROP TABLE IF EXISTS `Managers`;
    ''')
    cur.execute('''
      CREATE TABLE `Managers` (
        `manager_id` int(11) NOT NULL,
        `name` varchar(64) NOT NULL,
        `start_season` int(11) DEFAULT NULL,
        `team_id` int(11) DEFAULT NULL,
        PRIMARY KEY (`manager_id`),
        CONSTRAINT `manages` FOREIGN KEY (`team_id`) REFERENCES `Teams` (`team_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    )
    ''')
    conn.commit()
    # TODO: generate this data

'''Generates Grounds table'''
def grounds():
    cur.execute('''
        DROP TABLE IF EXISTS `Grounds`;
    ''')
    cur.execute('''
        CREATE TABLE `Grounds` (
          `grounds_id` int(11) NOT NULL,
          `team_id` int(11) DEFAULT NULL,
          `name` varchar(64) DEFAULT NULL,
          `city` varchar(64) DEFAULT NULL,
          `capacity` int(11) DEFAULT NULL,
          `pitch_length` int(11) DEFAULT NULL,
          `pitch_width` int(11) DEFAULT NULL,
          PRIMARY KEY (`grounds_id`),
          CONSTRAINT `owned by` FOREIGN KEY (`team_id`) REFERENCES `Teams` (`team_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
        )
    ''')
    conn.commit()
    #This data remains static
    grounds_data = [
        [1, 1, "Emirates Stadium", "Holloway", 60000, 68, 105],
        [2, 2, "Vitality Stadium", "Bournemouth", 11000, 78, 105],
        [3, 3, "Amex Stadium", "Falmer", 37000, 69, 105],
        [4, 4, "Turf Moor", "Burnley", 21000, 68, 105],
        [5, 5, "Stamford Bridge", "Fulham", 41000, 67, 103],
        [6, 6, "Selhurst Park", "Selhurst", 25000, 68, 101],
        [7, 7, "Goodison Park", "Liverpool", 39500, 68, 100],
        [8, 8, "John Smith's Stadium", "Huddersfield", 24000, 69, 105],
        [9, 9, "King Power Stadium", "Leicester", 32000, 68, 105],
        [10, 10, "Anfield", "Liverpool", 54000, 68, 101],
        [11, 11, "Etihad Stadium", "Manchester", 55000, 68, 105],
        [12, 12, "Old Trafford", "Manchester", 75000, 68, 105],
        [13, 13, "St. James' Park", "Newcastle upon Tyne", 52000, 68, 105],
        [14, 14, "St. Mary's Stadium", "Southampton", 32000, 68, 105],
        [15, 15, "bet365 Stadium", "Stoke-on-Trent", 30000, 68, 105],
        [16, 16, "Liberty Stadium", "Swansea", 21000, 68, 105],
        [17, 17, "Wembley", "London", 90000, 69, 105],
        [18, 18, "Vicarage Road", "Watford", 23700, 73, 110],
        [19, 19, "The Hawthorns", "West Bromwich", 26800, 68, 105],
        [20, 20, "London Stadium", "London", 60000, 68, 105]
    ]
    for g in grounds_data:
        cur.execute('''
            INSERT INTO Grounds (grounds_id, team_id, name, city, capacity, pitch_length, pitch_width)
            VALUES
            (?, ?, ?, ?, ?, ?, ?)''',
            tuple(g)
        )
        conn.commit()

'''Generates Referees table'''
def referees():
    cur.execute('''
        DROP TABLE IF EXISTS `Referees`;
    ''')
    cur.execute('''
        CREATE TABLE `Referees` (
          `ref_id` int(11) NOT NULL,
          `name` varchar(64) DEFAULT NULL,
          `original_county_fa` varchar(64) DEFAULT NULL,
          PRIMARY KEY (`ref_id`)
        )
    ''')
    conn.commit()
    # TODO: generate this data

'''Generates Awards table'''
def awards():
    cur.execute('''
        DROP TABLE IF EXISTS `Awards`;
    ''')
    cur.execute('''
        CREATE TABLE `Awards` (
          `month` varchar(32) NOT NULL,
          `player_id` int(11) DEFAULT NULL,
          `goal_id` int(11) DEFAULT NULL,
          `manager_id` int(11) DEFAULT NULL,
          PRIMARY KEY (`month`),
          CONSTRAINT `GotM` FOREIGN KEY (`goal_id`) REFERENCES `Goals` (`goal_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `MotM` FOREIGN KEY (`manager_id`) REFERENCES `Managers` (`manager_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `PotM` FOREIGN KEY (`player_id`) REFERENCES `Players` (`player_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
        )
    ''')
    conn.commit()
    #This data is hard coded in each month
    awards_data = [
        ['August',8,230,34],
	    ['September',11,394,34],
	    ['October',11,255,34],
    ]
    for a in awards_data:
        cur.execute('''
            INSERT INTO Awards (month, player_id, goal_id, manager_id)
            VALUES
            (?, ?, ?, ?)''',
            tuple(a)
        )
        conn.commit()
    # TODO: GoTM data is currently fictitious

'''From web'''
# SAVE THIS ADDR TO A LOCAL FILE IF YOU'RE SCRAPING MULTIPLE TIMES IN AN HOUR
# link="https://fantasy.premierleague.com/drf/bootstrap-static"
# data = urllib.request.urlopen(link)
# data = data.read().decode('utf-8')
# data = json.loads(data)

'''From local file'''
link='fpl.json'
data = open(link, encoding='utf-8').read()
data = json.loads(data)

'''Console Input'''
options = {
    'A':'Generate ALL tables',
    'B':'Print the JSON tree',
    'C':'Teams',
    'D':'Players',
    'E':'Fixtures',
    'F':'Cards',
    'G':'Goals',
    'H':'Managers',
    'I':'Grounds',
    'J':'Referees',
    'K':'Awards',
}
print("What you like to do?")
for k in sorted(options.keys()):
	if k=='A' or k=='B':
		print("  " + k + ") " + options[k])
	else:
		print("  " + k + ") Create " + options[k])
print("List letters (e.g. \"ABF\") or just hit \"return\" to generate ALL available tables")
choice = input("Your selection:")
if choice:
	choice = "".join(set(choice.upper()))
	for i in choice:
		if i =='A':
			for j in options:
				if(j != 'A' and j !='B'):
					print("  Generating " + options[j].lower() + "...")
					exec(options[j].lower() + "()")
		elif i =='B':
			key_tree(data, 0, False)
			print()
		elif i in options:
			print("  Generating " + options[i].lower() + "...")
			exec(options[i].lower() + "()")
		else:
			print("  ERROR: Your choice, \"" + i + "\", is not a valid option!")
	print("Done!")
else:
	for j in options:
		if(j != 'A' and j !='B'):
			print("  Generating " + options[j].lower() + "...")
			exec(options[j].lower() + "()")
	print("Done!")
