import sqlite3

def init_db(db_file):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS TEAMS (labelTeam text, placeTeam int, pointsTeam int, j int, d int, p int, c int, uNumGroup int)")
    cursor.execute("CREATE TABLE IF NOT EXISTS MATCHS (uNumMatch int, team1 text, team2 text, scoreMatch text, uNumRound int)")
    cursor.execute("CREATE TABLE IF NOT EXISTS GAMES (player1 text, elo1 int, player2 text, elo2 int, numBoard int, scoreGame text, uNumMatch int)")
    return db, cursor

def parse_teams(input_file, db_file):
    db, cursor = init_db(db_file)
    (group, division, compet, season) = ("", "", "", "")
    f = open(input_file, 'r')
    for line in f:
        if(line[-1:] is '\n'): line = line[:-1]
        if('group' in line):
            group = line.split('group:')[1].split(',')[0]
            division = line.split('division:')[1].split(',')[0]
            compet = line.split('compet:')[1].split(',')[0]
            season = line.split('season:')[1]
        else:
            (place, label, points, j, d, p, c) = line.split('\t')
            values= "('" + label + \
                    "'," + place + \
                    "," + points + \
                    "," + j + \
                    "," + d + \
                    "," + p + \
                    "," + c + \
                    "," + group + ")"
            cursor.execute("INSERT INTO TEAMS VALUES " + values)
            
    db.commit()
    db.close()
    return

def parse_round_details(input_file, db_file):
    db, cursor = init_db(db_file)
    teams = []
    for team_array in cursor.execute("SELECT labelTeam FROM TEAMS"):
        teams.append(team_array[0])

    f = open(input_file, 'r')
    num_match = 0
    (num_round, group, division, compet, season) = ("", "", "", "", "")
    for line in f:
        if(line[-1:] is '\n'): line = line[:-1]
        if(line[-1:] is '\t'): line = line[:-1]
        if(line is ''): continue
        if('group' in line):
            num_round = line.split('round:')[1].split(',')[0]
            group = line.split('group:')[1].split(',')[0]
            division = line.split('division:')[1].split(',')[0]
            compet = line.split('compet:')[1].split(',')[0]
            season = line.split('season:')[1]
        else:
            try:
                (actor1, score, actor2) = line.split('\t')
                if(actor1 in teams and actor2 in teams):
                    num_match += 1
                    values= "(" + str(num_match) + \
                            ",'" + actor1 + \
                            "','" + actor2 + \
                            "','" + score + \
                            "," + num_round + ")"
                    cursor.execute("INSERT INTO MATCHS VALUES " + values)
                else:
                    (player1, elo1) = actor1.rsplit(' ', 1)
                    (player2, elo2) = actor2.rsplit(' ', 1)
                    values= "('" + player1 + \
                            "'," + elo1 + \
                            ",'" + player2 + \
                            "'," + elo2 + \
                            "," + str(9999) + \
                            ",'" + score + \
                            "'," + str(num_match) + ")"
                    cursor.execute("INSERT INTO GAMES VALUES " + values)
            except: pass

    db.commit()
    db.close()
