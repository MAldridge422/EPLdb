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
    # TODO: scrape this data
    # This data generated. While it is the correct number of cards,
    # and has the right yellow/red ratio, it is a random distribution
    cards_data = [
      [1,0,60,340],
      [2,0,22,200],
      [3,0,89,451],
      [4,0,4,470],
      [5,0,88,90],
      [6,0,3,254],
      [7,0,54,115],
      [8,0,121,458],
      [9,0,88,378],
      [10,0,50,532],
      [11,0,7,565],
      [12,0,108,51],
      [13,0,42,427],
      [14,0,18,333],
      [15,0,64,10],
      [16,0,108,331],
      [17,0,50,304],
      [18,0,70,443],
      [19,0,112,485],
      [20,0,3,216],
      [21,0,55,482],
      [22,0,121,511],
      [23,0,65,480],
      [24,0,58,455],
      [25,0,73,378],
      [26,0,55,481],
      [27,0,91,94],
      [28,0,40,233],
      [29,0,15,390],
      [30,0,32,220],
      [31,0,130,278],
      [32,0,42,500],
      [33,0,85,261],
      [34,0,39,108],
      [35,0,6,189],
      [36,0,56,52],
      [37,0,52,344],
      [38,0,42,2],
      [39,0,74,42],
      [40,0,29,22],
      [41,0,23,11],
      [42,0,80,50],
      [43,0,71,564],
      [44,0,98,460],
      [45,0,15,213],
      [46,0,106,234],
      [47,0,79,213],
      [48,0,94,283],
      [49,0,105,344],
      [50,0,57,560],
      [51,0,31,153],
      [52,0,71,433],
      [53,0,37,111],
      [54,0,100,161],
      [55,0,82,129],
      [56,0,57,136],
      [57,0,71,416],
      [58,0,75,7],
      [59,0,94,213],
      [60,0,85,120],
      [61,0,57,17],
      [62,0,61,442],
      [63,0,91,6],
      [64,0,6,103],
      [65,0,37,418],
      [66,0,36,562],
      [67,0,13,93],
      [68,0,79,240],
      [69,0,95,530],
      [70,0,68,116],
      [71,0,52,154],
      [72,0,46,229],
      [73,0,109,494],
      [74,0,22,100],
      [75,0,119,113],
      [76,0,49,146],
      [77,0,41,428],
      [78,0,46,501],
      [79,0,42,104],
      [80,0,42,503],
      [81,0,75,419],
      [82,0,15,231],
      [83,0,1,538],
      [84,0,111,539],
      [85,0,19,544],
      [86,0,4,189],
      [87,0,49,141],
      [88,0,124,188],
      [89,0,8,72],
      [90,0,70,422],
      [91,0,118,520],
      [92,0,65,286],
      [93,0,75,34],
      [94,0,95,429],
      [95,0,122,564],
      [96,0,129,423],
      [97,0,54,421],
      [98,0,8,156],
      [99,0,72,49],
      [100,0,65,516],
      [101,0,93,233],
      [102,0,53,197],
      [103,0,76,126],
      [104,0,118,445],
      [105,0,58,481],
      [106,0,26,348],
      [107,0,49,455],
      [108,0,112,402],
      [109,0,91,400],
      [110,0,114,294],
      [111,0,43,370],
      [112,0,87,269],
      [113,0,106,125],
      [114,0,26,97],
      [115,0,59,251],
      [116,0,123,101],
      [117,0,123,501],
      [118,0,33,531],
      [119,0,6,98],
      [120,0,85,407],
      [121,0,81,428],
      [122,0,105,60],
      [123,0,52,8],
      [124,0,124,245],
      [125,0,97,383],
      [126,0,108,319],
      [127,0,89,554],
      [128,0,109,497],
      [129,0,60,412],
      [130,0,20,93],
      [131,0,94,81],
      [132,0,56,390],
      [133,0,112,289],
      [134,0,125,448],
      [135,0,109,42],
      [136,0,59,536],
      [137,0,113,366],
      [138,0,127,22],
      [139,0,56,438],
      [140,0,93,193],
      [141,0,130,337],
      [142,0,78,2],
      [143,0,1,404],
      [144,0,93,89],
      [145,0,112,145],
      [146,0,81,231],
      [147,0,47,278],
      [148,0,81,18],
      [149,0,119,232],
      [150,0,88,465],
      [151,0,103,139],
      [152,0,127,235],
      [153,0,29,417],
      [154,0,106,128],
      [155,0,88,81],
      [156,0,24,93],
      [157,0,17,457],
      [158,0,50,312],
      [159,0,69,184],
      [160,0,38,62],
      [161,0,110,375],
      [162,0,109,101],
      [163,0,36,474],
      [164,0,67,287],
      [165,0,31,314],
      [166,0,29,315],
      [167,0,69,518],
      [168,0,50,378],
      [169,0,30,60],
      [170,0,82,196],
      [171,0,11,306],
      [172,0,53,373],
      [173,0,80,139],
      [174,0,60,112],
      [175,0,111,402],
      [176,0,104,182],
      [177,0,10,30],
      [178,0,30,177],
      [179,0,118,134],
      [180,0,105,202],
      [181,0,49,292],
      [182,0,11,31],
      [183,0,92,73],
      [184,0,101,135],
      [185,0,75,447],
      [186,0,44,223],
      [187,0,76,134],
      [188,0,83,127],
      [189,0,101,24],
      [190,0,67,248],
      [191,0,30,369],
      [192,0,127,369],
      [193,0,37,384],
      [194,0,34,507],
      [195,0,69,9],
      [196,0,67,402],
      [197,0,113,304],
      [198,0,56,361],
      [199,0,130,177],
      [200,0,68,117],
      [201,0,63,522],
      [202,0,84,262],
      [203,0,56,161],
      [204,0,47,542],
      [205,0,74,552],
      [206,0,38,358],
      [207,0,39,329],
      [208,0,57,516],
      [209,0,101,546],
      [210,0,9,477],
      [211,0,121,559],
      [212,0,94,203],
      [213,0,85,333],
      [214,0,128,221],
      [215,0,129,102],
      [216,0,104,10],
      [217,0,104,509],
      [218,0,78,501],
      [219,0,123,180],
      [220,0,97,110],
      [221,0,85,408],
      [222,0,129,377],
      [223,0,27,548],
      [224,0,44,180],
      [225,0,52,530],
      [226,0,8,484],
      [227,0,31,162],
      [228,0,47,159],
      [229,0,26,282],
      [230,0,104,76],
      [231,0,96,326],
      [232,0,108,64],
      [233,0,49,287],
      [234,0,27,420],
      [235,0,61,147],
      [236,0,2,39],
      [237,0,7,54],
      [238,0,115,536],
      [239,0,95,479],
      [240,0,108,365],
      [241,0,40,526],
      [242,0,30,371],
      [243,0,38,398],
      [244,0,106,330],
      [245,0,1,480],
      [246,0,78,546],
      [247,0,2,90],
      [248,0,87,214],
      [249,0,24,215],
      [250,0,48,473],
      [251,0,128,175],
      [252,0,84,65],
      [253,0,125,126],
      [254,0,28,554],
      [255,0,15,62],
      [256,0,130,212],
      [257,0,71,192],
      [258,0,25,394],
      [259,0,113,435],
      [260,0,24,539],
      [261,0,28,164],
      [262,0,24,499],
      [263,0,100,472],
      [264,0,38,284],
      [265,0,115,99],
      [266,0,45,252],
      [267,0,119,533],
      [268,0,55,378],
      [269,0,21,499],
      [270,0,65,2],
      [271,0,11,85],
      [272,0,85,184],
      [273,0,5,256],
      [274,0,125,332],
      [275,0,125,43],
      [276,0,119,55],
      [277,0,107,309],
      [278,0,44,482],
      [279,0,105,387],
      [280,0,66,561],
      [281,0,17,563],
      [282,0,106,473],
      [283,0,96,219],
      [284,0,54,470],
      [285,0,4,459],
      [286,0,11,376],
      [287,0,9,536],
      [288,0,115,289],
      [289,0,87,543],
      [290,0,47,255],
      [291,0,51,353],
      [292,0,17,74],
      [293,0,12,477],
      [294,0,92,345],
      [295,0,103,266],
      [296,0,37,271],
      [297,0,82,530],
      [298,0,75,456],
      [299,0,76,173],
      [300,0,23,23],
      [301,0,39,494],
      [302,0,23,2],
      [303,0,12,194],
      [304,0,122,522],
      [305,0,86,285],
      [306,0,99,198],
      [307,0,127,236],
      [308,0,43,482],
      [309,0,99,218],
      [310,0,64,460],
      [311,0,64,552],
      [312,0,130,145],
      [313,0,89,571],
      [314,0,56,168],
      [315,0,80,267],
      [316,0,18,1],
      [317,0,17,541],
      [318,0,31,252],
      [319,0,129,52],
      [320,0,34,506],
      [321,0,68,147],
      [322,0,40,61],
      [323,0,59,140],
      [324,0,52,408],
      [325,0,71,139],
      [326,0,128,306],
      [327,0,36,482],
      [328,0,13,98],
      [329,0,98,161],
      [330,0,21,495],
      [331,0,53,558],
      [332,0,99,160],
      [333,0,108,29],
      [334,0,119,380],
      [335,0,48,514],
      [336,0,48,99],
      [337,0,117,359],
      [338,0,90,475],
      [339,0,114,542],
      [340,0,71,158],
      [341,0,101,471],
      [342,0,125,487],
      [343,0,82,540],
      [344,0,63,346],
      [345,0,107,463],
      [346,0,124,200],
      [347,0,21,26],
      [348,0,32,232],
      [349,0,84,175],
      [350,0,44,266],
      [351,0,78,195],
      [352,0,2,132],
      [353,0,77,489],
      [354,0,28,119],
      [355,0,23,343],
      [356,0,114,327],
      [357,0,127,200],
      [358,0,49,353],
      [359,0,35,194],
      [360,0,88,297],
      [361,0,18,219],
      [362,0,81,186],
      [363,0,5,16],
      [364,0,103,401],
      [365,0,1,83],
      [366,0,88,227],
      [367,0,85,93],
      [368,0,109,355],
      [369,0,130,242],
      [370,0,2,13],
      [371,0,117,434],
      [372,0,76,452],
      [373,0,92,27],
      [374,0,9,491],
      [375,0,67,437],
      [376,0,117,342],
      [377,0,35,368],
      [378,0,75,310],
      [379,0,25,67],
      [380,0,60,285],
      [381,0,62,364],
      [382,0,20,276],
      [383,0,9,521],
      [384,0,84,523],
      [385,0,102,149],
      [386,0,7,148],
      [387,0,2,365],
      [388,0,53,203],
      [389,0,74,552],
      [390,0,130,383],
      [391,0,59,428],
      [392,0,80,488],
      [393,0,108,426],
      [394,0,84,385],
      [395,0,92,41],
      [396,0,49,104],
      [397,0,31,477],
      [398,0,125,502],
      [399,0,121,206],
      [400,1,130,141],
      [401,1,72,301],
      [402,1,113,185],
      [403,1,23,562],
      [404,1,94,393],
      [405,1,109,222],
      [406,1,92,207],
      [407,1,41,321],
      [408,1,115,283],
      [409,1,81,60],
      [410,1,20,395],
      [411,1,59,256],
      [412,1,10,70],
      [413,1,20,169],
      [414,1,7,438],
      [415,1,119,391],
      [416,1,47,244],
      [417,1,122,26],
      [418,1,11,119],
      [419,1,26,560],
      [420,1,39,495],
      [421,1,19,98],
      [422,1,114,153],
      [423,1,70,549],
      [424,1,65,20],
      [425,1,110,352],
      [426,1,72,415],
      [427,1,80,313],
      [428,1,24,415],
      [429,1,91,292],
      [430,1,59,63],
      [431,1,38,31],
      [432,1,50,217],
      [433,1,8,546],
      [434,1,22,339],
      [435,1,22,289],
      [436,1,59,224],
      [437,1,87,435],
      [438,1,15,487],
      [439,1,16,228],
    ]
    for c in cards_data:
        cur.execute('''
            INSERT INTO Cards (card_id, is_red, fixture_id, player_id)
            VALUES
            (?, ?, ?, ?)''',
            tuple(c)
        )
        conn.commit()


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
    # TODO: scrape this data
    # This data generated. While it is the correct number of goals,
    # it is a random distribution
    goals_data = [
      [1,219,4,106],
      [2,498,12,49],
      [3,348,17,129],
      [4,510,5,110],
      [5,507,5,118],
      [6,78,10,77],
      [7,468,1,56],
      [8,11,7,35],
      [9,521,12,65],
      [10,569,16,52],
      [11,544,16,122],
      [12,511,2,75],
      [13,90,6,24],
      [14,107,17,116],
      [15,232,15,81],
      [16,236,18,67],
      [17,24,15,38],
      [18,445,5,123],
      [19,203,18,72],
      [20,173,4,102],
      [21,186,2,113],
      [22,178,6,127],
      [23,470,14,38],
      [24,256,9,36],
      [25,546,20,86],
      [26,2,1,128],
      [27,88,8,18],
      [28,257,15,38],
      [29,404,10,128],
      [30,571,5,95],
      [31,331,4,83],
      [32,81,13,121],
      [33,332,14,4],
      [34,537,20,55],
      [35,75,18,39],
      [36,164,18,79],
      [37,246,14,115],
      [38,370,12,17],
      [39,228,10,116],
      [40,14,1,42],
      [41,448,14,116],
      [42,147,3,122],
      [43,44,10,90],
      [44,219,15,8],
      [45,257,4,20],
      [46,438,16,31],
      [47,227,9,113],
      [48,536,14,91],
      [49,276,12,5],
      [50,93,17,127],
      [51,36,14,21],
      [52,123,19,72],
      [53,252,13,46],
      [54,562,16,79],
      [55,204,1,126],
      [56,169,20,29],
      [57,234,20,17],
      [58,568,7,111],
      [59,344,20,122],
      [60,464,2,60],
      [61,8,20,33],
      [62,165,12,78],
      [63,266,16,69],
      [64,111,3,96],
      [65,291,7,126],
      [66,130,12,11],
      [67,529,8,63],
      [68,254,5,128],
      [69,545,9,32],
      [70,184,18,41],
      [71,512,2,53],
      [72,28,3,82],
      [73,338,2,4],
      [74,390,6,33],
      [75,510,8,71],
      [76,518,2,72],
      [77,237,17,88],
      [78,216,18,40],
      [79,522,17,79],
      [80,491,16,32],
      [81,442,16,38],
      [82,184,19,82],
      [83,470,8,14],
      [84,309,7,51],
      [85,502,6,59],
      [86,280,18,97],
      [87,280,6,123],
      [88,31,3,7],
      [89,145,6,38],
      [90,324,7,94],
      [91,23,18,121],
      [92,82,11,92],
      [93,317,11,47],
      [94,153,8,103],
      [95,299,20,128],
      [96,227,11,125],
      [97,481,10,84],
      [98,16,10,122],
      [99,130,17,61],
      [100,56,4,22],
      [101,174,12,82],
      [102,97,16,4],
      [103,354,2,121],
      [104,174,6,59],
      [105,43,3,116],
      [106,276,15,107],
      [107,493,5,8],
      [108,323,13,106],
      [109,97,15,8],
      [110,307,17,29],
      [111,73,9,81],
      [112,426,5,123],
      [113,509,5,36],
      [114,483,8,4],
      [115,34,10,129],
      [116,205,1,86],
      [117,111,7,121],
      [118,120,8,95],
      [119,234,18,47],
      [120,558,3,6],
      [121,82,3,115],
      [122,361,15,94],
      [123,297,15,63],
      [124,418,20,121],
      [125,112,18,95],
      [126,556,2,68],
      [127,31,19,125],
      [128,483,19,58],
      [129,216,9,21],
      [130,130,12,81],
      [131,182,18,114],
      [132,560,8,116],
      [133,441,6,19],
      [134,508,20,101],
      [135,401,18,29],
      [136,228,7,24],
      [137,541,15,110],
      [138,378,4,50],
      [139,490,11,38],
      [140,238,20,103],
      [141,383,17,95],
      [142,75,6,16],
      [143,249,9,95],
      [144,132,8,28],
      [145,514,5,57],
      [146,230,10,79],
      [147,307,3,40],
      [148,426,11,86],
      [149,454,18,18],
      [150,163,11,99],
      [151,137,6,42],
      [152,297,3,20],
      [153,269,1,129],
      [154,59,16,15],
      [155,248,17,101],
      [156,516,17,126],
      [157,551,8,106],
      [158,220,10,87],
      [159,311,5,120],
      [160,201,7,91],
      [161,103,4,62],
      [162,321,8,91],
      [163,477,11,6],
      [164,23,15,89],
      [165,570,18,7],
      [166,4,15,91],
      [167,323,16,36],
      [168,207,12,93],
      [169,219,17,11],
      [170,327,6,114],
      [171,20,18,44],
      [172,41,19,43],
      [173,258,7,118],
      [174,396,17,5],
      [175,296,13,57],
      [176,222,16,48],
      [177,99,14,55],
      [178,330,14,121],
      [179,100,20,15],
      [180,53,3,39],
      [181,409,2,70],
      [182,193,16,99],
      [183,119,7,120],
      [184,72,10,113],
      [185,503,1,65],
      [186,412,2,96],
      [187,313,15,29],
      [188,346,7,10],
      [189,63,10,27],
      [190,55,12,3],
      [191,136,6,113],
      [192,543,19,41],
      [193,217,4,106],
      [194,276,13,74],
      [195,503,7,13],
      [196,567,9,70],
      [197,569,2,11],
      [198,319,10,66],
      [199,74,9,8],
      [200,94,12,105],
      [201,397,15,52],
      [202,523,4,70],
      [203,521,4,59],
      [204,427,17,9],
      [205,371,8,90],
      [206,294,20,77],
      [207,352,15,64],
      [208,562,5,91],
      [209,180,5,19],
      [210,112,1,58],
      [211,71,12,57],
      [212,465,18,20],
      [213,63,2,62],
      [214,61,19,70],
      [215,234,20,100],
      [216,190,4,50],
      [217,138,18,118],
      [218,52,3,98],
      [219,410,17,127],
      [220,269,4,100],
      [221,370,8,43],
      [222,110,5,55],
      [223,297,13,100],
      [224,283,5,120],
      [225,538,20,16],
      [226,535,5,115],
      [227,52,15,47],
      [228,270,15,74],
      [229,561,15,104],
      [230,437,15,62],
      [231,75,7,9],
      [232,92,5,90],
      [233,169,9,35],
      [234,73,6,69],
      [235,93,3,85],
      [236,502,17,55],
      [237,331,19,100],
      [238,24,4,26],
      [239,434,12,104],
      [240,81,3,13],
      [241,182,6,124],
      [242,91,13,110],
      [243,477,18,105],
      [244,76,10,4],
      [245,558,4,28],
      [246,281,19,71],
      [247,6,3,62],
      [248,187,17,7],
      [249,82,19,33],
      [250,177,8,97],
      [251,423,7,81],
      [252,302,12,116],
      [253,250,20,13],
      [254,408,3,128],
      [255,170,17,105],
      [256,512,12,113],
      [257,361,9,47],
      [258,412,13,128],
      [259,140,14,49],
      [260,76,16,69],
      [261,265,4,8],
      [262,157,12,25],
      [263,222,3,91],
      [264,43,12,87],
      [265,315,10,120],
      [266,314,3,27],
      [267,310,2,36],
      [268,539,3,122],
      [269,96,14,65],
      [270,119,7,41],
      [271,95,3,105],
      [272,308,17,66],
      [273,444,10,61],
      [274,36,13,91],
      [275,37,14,4],
      [276,393,9,87],
      [277,483,1,129],
      [278,396,20,47],
      [279,297,15,99],
      [280,45,11,65],
      [281,145,8,41],
      [282,17,19,42],
      [283,567,19,38],
      [284,424,16,44],
      [285,534,16,54],
      [286,539,19,21],
      [287,379,2,108],
      [288,206,11,45],
      [289,480,8,120],
      [290,395,14,30],
      [291,202,4,31],
      [292,12,16,61],
      [293,8,17,89],
      [294,20,3,102],
      [295,526,11,119],
      [296,215,2,71],
      [297,6,12,78],
      [298,227,13,67],
      [299,270,7,21],
      [300,86,18,58],
      [301,513,14,90],
      [302,322,16,130],
      [303,376,2,48],
      [304,202,3,52],
      [305,462,8,123],
      [306,65,20,89],
      [307,459,11,68],
      [308,21,13,51],
      [309,461,8,18],
      [310,200,18,25],
      [311,525,16,18],
      [312,429,13,17],
      [313,36,11,50],
      [314,93,4,70],
      [315,124,16,99],
      [316,383,17,64],
      [317,523,14,109],
      [318,167,13,71],
      [319,167,7,62],
      [320,392,13,43],
      [321,412,16,127],
      [322,98,18,6],
      [323,417,15,27],
      [324,228,1,66],
      [325,415,16,54],
      [326,60,11,84],
      [327,398,3,12],
      [328,172,18,18],
      [329,320,5,3],
      [330,146,14,121],
      [331,557,19,67],
      [332,91,9,48],
      [333,184,17,6],
      [334,73,2,17],
      [335,228,14,38],
      [336,224,7,66],
      [337,545,11,42],
    ]
    for g in goals_data:
        cur.execute('''
            INSERT INTO Goals (goal_id, player_id, team_id, fixture_id)
            VALUES
            (?, ?, ?, ?)''',
            tuple(g)
        )
        conn.commit()

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
    managers_data = [
      [1, "Arsene Wenger", 1, 1996],
      [2, "Eddie Howe", 2, 2012],
      [3, "Chris Hughton", 3, 2014],
      [4, "Sean Dyche", 4, 2012],
      [5, "Antonio Conte", 5, 2016],
      [6, "Roy Hodgson", 6, 2017],
      [7, "Sam Allardyce", 7, 2017],
      [8, "David Wagner", 8, 2015],
      [9, "Claude Puel", 9, 2017],
      [10, "Jurgen Klopp", 10, 2015],
      [11, "Josep Guardiola", 11, 2016],
      [12, "Jose Mourinho", 12, 2016],
      [13, "Rafael Benitez", 13, 2016],
      [14, "Mauricio Pellegrino", 14, 2017],
      [15, "Mark Hughes", 15, 2013],
      [16, "Paul Clement", 16, 2017],
      [17, "Mauricio Pochettino", 17, 2014],
      [18, "Marco Silva", 18, 2017],
      [19, "Alan Pardew", 19, 2017],
      [20, "David Moyes", 20, 2017],
    ]
    for m in managers_data:
        cur.execute('''
            INSERT INTO Managers (manager_id, name, team_id, start_season)
            VALUES
            (?, ?, ?, ?)''',
            tuple(m)
        )
        conn.commit()


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
          `pitch_width` int(11) DEFAULT NULL,
          `pitch_length` int(11) DEFAULT NULL,
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
            INSERT INTO Grounds (grounds_id, team_id, name, city, capacity, pitch_width, pitch_length)
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
          `manager_id` int(11) DEFAULT NULL,
          `goal_id` int(11) DEFAULT NULL,
          `player_id` int(11) DEFAULT NULL,
          PRIMARY KEY (`month`),
          CONSTRAINT `GotM` FOREIGN KEY (`goal_id`) REFERENCES `Goals` (`goal_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `MotM` FOREIGN KEY (`manager_id`) REFERENCES `Managers` (`manager_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `PotM` FOREIGN KEY (`player_id`) REFERENCES `Players` (`player_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
        )
    ''')
    conn.commit()
    #This data is hard coded in each month
    awards_data = [
        ['August',8,230,20],
	    ['September',11,394,324],
	    ['October',11,255,157],
    ]
    for a in awards_data:
        cur.execute('''
            INSERT INTO Awards (month, manager_id, goal_id, player_id)
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
