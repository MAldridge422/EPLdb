import json
import urllib.request

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

'''Simple print to csv file func'''
def print_csv(args, file=None):
	line = ""
	for i in range(0, len(args)):
		if(isinstance(args[i], int)):
			line += str(args[i])
		else:
			line += "\"" + args[i] + "\""
		if i != len(args)-1:
			line += ","
	if file != None:
		# TODO: UTF-8 encoding
		output = open(file, 'a')
		print(line, file=output)
	else:
		print(line)

'''Generates teams.csv'''
def teams_csv():
	output = 'teams2.csv'
	open(output, 'w').close() #clear the file
	nicknames = {
		'ARS':'Gunners',
		'BOU':'Poppers',
		'BHA':'Seagulls',
		'BUR':'Clarets',
		'CHE':'Blues',
		'CRY':'Eagles',
		'EVE':'Toffees',
		'HUD':"Terriers",
	  "LEI": "Foxes",
	  "LIV": "Reds",
	  "MCI": "Citizens",
	  "MUN": "Red Devils",
	  "NEW": "Magpies",
	  "SOU": "Saints",
	  "STK": "Potters",
	  "SWA": "Swans",
	  "TOT": "Spurs",
	  "WAT": "Hornets",
	  "WBA": "Baggies",
	  "WHU": "Hammers",
	}
	#Header row
	print_csv(["team_id", "abbrev", "full_name", "nickname"], file=output)
	teams = data['teams']
	for t in teams:
		team_id = int(t['id'])
		name = t['name']
		code = int(t['code'])
		abbrev = t['short_name']
		nickname = nicknames[abbrev]
		print_csv([team_id, abbrev, name, nickname], file=output)

'''Generates players.csv'''
def players_csv():
	output = 'players2.csv'
	open(output, 'w').close() #clear the file
	positions = {
		1:"GoalKeeper",
		2:"Defender",
		3:"Midfielder",
		4:"Forward"
	}
	players = data['elements']
	#Header row
	print_csv(["player_id", "name", "position", "minutes_played", "assists", "saves", "team_id"], file=output)
	for p in players:
		player_id = int(p['id'])
		name = p['web_name']
		position = positions[p['element_type']]
		minutes_played = int(p['minutes'])
		assists = int(p['assists'])
		saves = int(p['saves'])
		team_id = p['team']
		print_csv([player_id, name, position, minutes_played, assists, saves, team_id], file=output)

'''Generates fixtures.csv'''
def fixtures_csv():
	pass

'''Generates cards.csv'''
def cards_csv():
	pass

'''Generates goals.csv'''
def goals_csv():
	pass

'''Generates managers.csv'''
def managers_csv():
	pass

'''Generates grounds.csv'''
def grounds_csv():
	output = 'grounds2.csv'
	open(output, 'w').close() #clear the file
	#Header row
	print_csv(["ground_id", "team_id", "name", "city", "capacity", "pitch_width", "pitch_length"], file=output)
	#This data remains static
	print_csv([1, 1, "Emirates Stadium", "Holloway", 60000, 68, 105], file=output)
	print_csv([2, 2, "Vitality Stadium", "Bournemouth", 11000, 78, 105], file=output)
	print_csv([3, 3, "Amex Stadium", "Falmer", 37000, 69, 105], file=output)
	print_csv([4, 4, "Turf Moor", "Burnley", 21000, 68, 105], file=output)
	print_csv([5, 5, "Stamford Bridge", "Fulham", 41000, 67, 103], file=output)
	print_csv([6, 6, "Selhurst Park", "Selhurst", 25000, 68, 101], file=output)
	print_csv([7, 7, "Goodison Park", "Liverpool", 39500, 68, 100], file=output)
	print_csv([8, 8, "John Smith's Stadium", "Huddersfield", 24000, 69, 105], file=output)
	print_csv([9, 9, "King Power Stadium", "Leicester", 32000, 68, 105], file=output)
	print_csv([10, 10, "Anfield", "Liverpool", 54000, 68, 101], file=output)
	print_csv([11, 11, "Etihad Stadium", "Manchester", 55000, 68, 105], file=output)
	print_csv([12, 12, "Old Trafford", "Manchester", 75000, 68, 105], file=output)
	print_csv([13, 13, "St. James' Park", "Newcastle upon Tyne", 52000, 68, 105], file=output)
	print_csv([14, 14, "St. Mary's Stadium", "Southampton", 32000, 68, 105], file=output)
	print_csv([15, 15, "bet365 Stadium", "Stoke-on-Trent", 30000, 68, 105], file=output)
	print_csv([16, 16, "Liberty Stadium", "Swansea", 21000, 68, 105], file=output)
	print_csv([17, 17, "Wembley", "London", 90000, 69, 105], file=output)
	print_csv([18, 18, "Vicarage Road", "Watford", 23700, 73, 110], file=output)
	print_csv([19, 19, "The Hawthorns", "West Bromwich", 26800, 68, 105], file=output)
	print_csv([20, 20, "London Stadium", "London", 60000, 68, 105], file=output)

'''Generates referees.csv'''
def referees_csv():
	pass

'''Generates awards.csv'''
def awards_csv():
	#Header row
	print_csv(["month", "MotM", "PotM", "GotM"], file=output)
	#This data is hard coded in each month
	output = 'awards2.csv'
	open(output, 'w').close() #clear the file
	print_csv(['August',8,230,34], file=output)

'''From web'''
# SAVE THIS ADDR TO A LOCAL FILE IF YOU'RE SCRAPING MULTIPLE TIMES IN AN HOUR
# link="https://fantasy.premierleague.com/drf/bootstrap-static"
# data = urllib.request.urlopen(link)
# data = data.read().decode('utf-8')
# data = json.loads(data)

'''From local file'''
link='fpl_json.txt'
data = open(link, encoding='utf-8').read()
data = json.loads(data)

'''Console Input'''
options = {
  'A':'Generate ALL available .csv\'s',
  'B':'Print the JSON tree',
	'C':'teams',
	'D':'players',
	'E':'fixtures',
	'F':'cards',
	'G':'goals',
	'H':'managers',
	'I':'grounds',
	'J':'referees',
	'K':'awards',
}
print("What you like to do?")
for k in options.keys():
	if k=='A' or k=='B':
		print("  " + k + ") " + options[k])
	else:
		print("  " + k + ") Create " + options[k] + ".csv")
print("List letters (e.g. \"ABF\") or just hit \"return\" to generate ALL available .csv's")
choice = input("Your selection:")
if choice:
	choice = "".join(set(choice.upper()))
	for i in choice:
		if i =='A':
			for j in options:
				if(j != 'A' and j !='B'):
					print("  Generating " + options[j].lower() + ".csv...")
					exec(options[j].lower() + "_csv()")
		elif i =='B':
			key_tree(data, 0, False)
			print()
		elif i in options:
			print("  Generating " + options[i].lower() + ".csv...")
			exec(options[i].lower() + "_csv()")
		else:
			print("  ERROR: Your choice, \"" + i + "\", is not a valid option!")
	print("Done!")
else:
	for j in options:
		if(j != 'A' and j !='B'):
			print("  Generating " + options[j].lower() + ".csv...")
			exec(options[j].lower() + "_csv()")
	print("Done!")