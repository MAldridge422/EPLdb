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
    # this data needs to be periodically updated
    # TODO: automate this
    fixtures_data = [
        [1,1,9,4,3,1,6],
        [2,3,11,0,2,11,4],
        [3,5,4,2,3,4,5],
        [4,6,8,0,3,8,3],
        [5,7,15,1,0,7,8],
        [6,14,16,0,0,None,14],
        [7,18,10,3,3,None,1],
        [8,19,2,1,0,19,10],
        [9,12,20,4,0,12,9],
        [10,13,17,0,2,17,2],
        [11,2,18,0,2,18,12],
        [12,4,19,0,1,19,9],
        [13,9,3,2,0,9,16],
        [14,10,6,1,0,10,13],
        [15,14,20,3,2,14,7],
        [16,15,1,1,0,15,2],
        [17,16,12,0,4,12,3],
        [18,8,13,1,0,8,5],
        [19,17,5,1,2,5,1],
        [20,11,7,1,1,None,10],
        [21,2,11,1,2,11,6],
        [22,6,16,0,2,16,2],
        [23,8,14,0,0,None,11],
        [24,12,9,2,0,12,4],
        [25,13,20,3,0,13,8],
        [26,18,3,0,0,None,17],
        [27,5,7,2,0,5,3],
        [28,10,1,4,0,10,5],
        [29,17,4,1,1,None,7],
        [30,19,15,1,1,None,1],
        [31,1,2,3,0,1,1],
        [32,3,19,3,1,3,15],
        [33,7,17,0,3,17,17],
        [34,9,5,1,2,5,7],
        [35,11,10,5,0,11,3],
        [36,14,18,0,2,18,16],
        [37,15,12,2,2,None,8],
        [38,4,6,1,0,4,4],
        [39,16,13,0,1,13,14],
        [40,20,8,2,0,20,13],
        [41,2,3,2,1,2,5],
        [42,6,14,0,1,14,10],
        [43,8,9,1,1,None,3],
        [44,10,4,1,1,None,12],
        [45,13,15,2,1,13,11],
        [46,17,16,0,0,None,6],
        [47,18,11,0,6,11,1],
        [48,19,20,0,0,None,18],
        [49,5,1,0,0,None,4],
        [50,12,7,4,0,12,2],
        [51,4,8,0,0,None,15],
        [52,7,2,2,1,7,9],
        [53,9,10,2,3,10,1],
        [54,11,6,5,0,11,8],
        [55,14,12,0,1,12,5],
        [56,15,5,0,4,5,6],
        [57,16,18,1,2,18,7],
        [58,20,17,2,3,17,4],
        [59,3,13,1,0,3,2],
        [60,1,19,2,0,1,10],
        [61,2,9,0,0,None,17],
        [62,5,11,0,1,11,9],
        [63,8,17,0,4,17,8],
        [64,12,6,4,0,12,6],
        [65,15,14,2,1,15,14],
        [66,19,18,2,2,None,4],
        [67,20,16,1,0,20,12],
        [68,1,3,2,0,1,13],
        [69,7,4,0,1,4,3],
        [70,13,10,1,1,None,5],
        [71,4,20,1,1,None,11],
        [72,6,5,2,1,6,2],
        [73,10,12,0,0,None,9],
        [74,11,15,7,2,11,5],
        [75,16,8,2,0,16,18],
        [76,17,2,1,0,17,10],
        [77,18,1,2,1,18,8],
        [78,3,7,1,1,None,4],
        [79,14,13,2,2,None,13],
        [80,9,19,1,1,None,6],
        [81,20,3,0,3,3,9],
        [82,5,18,4,2,5,3],
        [83,8,12,2,1,8,7],
        [84,11,4,3,0,11,12],
        [85,13,6,1,0,13,11],
        [86,14,19,1,0,14,17],
        [87,15,2,1,2,2,16],
        [88,16,9,1,2,9,4],
        [89,7,1,2,5,1,5],
        [90,17,10,4,1,17,2],
        [91,1,16,2,1,1,7],
        [92,2,5,0,1,5,5],
        [93,6,20,2,2,None,10],
        [94,10,8,3,0,10,13],
        [95,12,17,1,0,12,3],
        [96,18,15,0,1,15,4],
        [97,19,11,2,3,11,14],
        [98,3,14,1,1,None,8],
        [99,9,7,2,0,9,2],
        [100,4,13,1,0,4,6],
        [101,8,19,1,0,8,12],
        [102,13,2,0,1,2,18],
        [103,14,4,0,1,4,16],
        [104,15,9,2,2,None,10],
        [105,16,3,0,1,3,6],
        [106,20,10,1,4,10,8],
        [107,5,12,1,0,5,1],
        [108,7,18,3,2,7,17],
        [109,11,1,3,1,11,4],
        [110,17,6,1,0,17,13],
        [111,1,17,2,0,1,6],
        [112,2,8,4,0,2,16],
        [113,4,16,2,0,4,9],
        [114,6,7,2,2,None,1],
        [115,9,11,0,2,11,17],
        [116,10,14,3,0,10,14],
        [117,12,13,4,1,12,5],
        [118,19,5,0,4,5,3],
        [119,18,20,2,0,18,2],
        [120,3,15,2,2,None,7],
        [121,20,9,1,1,None,9],
        [122,6,15,2,1,6,6],
        [123,10,5,1,1,None,4],
        [124,12,3,1,0,12,8],
        [125,13,18,0,3,18,15],
        [126,16,2,0,0,None,11],
        [127,17,19,1,1,None,14],
        [128,4,1,0,1,1,7],
        [129,8,11,1,2,11,5],
        [130,14,7,4,1,14,13],
    ]
    for f in fixtures_data:
        cur.execute('''
            INSERT INTO Fixtures (fixture_id, home_team, away_team, home_goals, away_goals, winner_id, referee_id)
            VALUES
            (?, ?, ?, ?, ?, ?, ?)''',
            tuple(f)
        )
        conn.commit()

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
    #This data remains static
    refs_data = [
        [1,"Anthony Taylor","Cheshire"],
        [2,"Andre Marriner","Birmingham County"],
        [3,"Jonathan Moss","West Riding County"],
        [4,"Michael Oliver","Northumberland County"],
        [5,"Craig Pawson","Sheffield & Hallamshire"],
        [6,"Mike Dean","Cheshire"],
        [7,"Lee Mason","Lancashire"],
        [8,"Neil Swarbrick","Lancashire"],
        [9,"Martin Atkinson","West Riding County"],
        [10,"Robert Madley","West Riding County"],
        [11,"Stuart Attwell","Warwickshire"],
        [12,"Roger East","Wiltshire"],
        [13,"Kevin Friend","Leicestershire"],
        [14,"Mike Jones","Cheshire"],
        [15,"Chris Kavanagh","Manchester"],
        [16,"Lee Probert","Wiltshire"],
        [17,"Graham Scott","Berks & Bucks"],
        [18,"Paul Tierney","Lancashire"],
    ]
    for r in refs_data:
        cur.execute('''
            INSERT INTO Referees (ref_id, name, original_county_fa)
            VALUES
            (?, ?, ?)''',
            tuple(r)
        )
        conn.commit()

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
