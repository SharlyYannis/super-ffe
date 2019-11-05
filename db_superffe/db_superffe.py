import sqlite3

def _init_db(db_file):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS TEAMS (labelTeam text, placeTeam int, pointsTeam int, j int, d int, p int, c int, uidGroup text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS ROUNDS (uidRound text, numRound int, uidGroup text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS MATCHS (uidMatch text, team1 text, team2 text, scoreMatch text, uidRound text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS GAMES (player1 text, elo1 int, player2 text, elo2 int, numBoard int, scoreGame text, uidMatch text)")
    return db, cursor

def _close_and_commit(db):
    db.commit()
    db.close()

def _concat_game_values(actor1, actor2, board, score, uidMatch):
    (player1, elo1) = actor1.rsplit(' ', 1)
    (player2, elo2) = actor2.rsplit(' ', 1)
    return "('" + player1 + "'," + elo1 + ",'" + player2 + "'," + elo2 + \
            "," + str(board) + ",'" + score + "','" + uidMatch + "')"

def _concat_match_values(uidMatch, actor1, actor2, score, num_round):
    return "('" + uidMatch + "','" + actor1 + "','" + actor2 + \
            "','" + score + "','" + num_round + "')"

def _concat_team_values(line, group):
    (place, label, points, j, d, p, c) = line.split('\t')
    return "('" + label + "'," + place + "," + points + "," + j + \
            "," + d + "," + p + "," + c + ",'" + group + "')"

def _concat_round_values(uidRound, num_round, uidGroup):
    return "('" + uidRound + "'," + num_round + ",'" + uidGroup + "')"

def _split_descriptor(line):
    group = line.split('group:')[1].split(',')[0]
    division = line.split('division:')[1].split(',')[0]
    compet = line.split('compet:')[1].split(',')[0]
    season = line.split('season:')[1]
    return (group, division, compet, season)
   
def get_team_labels(cursor):
    teams = []
    for team_array in cursor.execute("SELECT labelTeam FROM TEAMS"):
        teams.append(team_array[0])
    return teams

def create_db(db_file):
    db, cursor = _init_db(db_file)
    _close_and_commit(db)

def parse_teams(input_file, db_file):
    db, cursor = _init_db(db_file)
    (group, division, compet, season) = ("", "", "", "")
    for line in open(input_file, 'r'):
        if(line[-1:] is '\n'): line = line[:-1]
        if('group' in line):
            (group, division, compet, season) = _split_descriptor(line)
            uidGroup = season+'_'+compet+'_'+division+'_'+group
        else:
            values = _concat_team_values(line, uidGroup)
            cursor.execute("INSERT INTO TEAMS VALUES " + values)
    _close_and_commit(db)            

def parse_round_details(input_file, db_file):
    db, cursor = _init_db(db_file)
    teams = get_team_labels(cursor)
    num_round = ""
    num_match = 0
    for line in open(input_file, 'r'):
        try:
            if(line[-1:] is '\n'): line = line[:-1]
            if(line[-1:] is '\t'): line = line[:-1]
            if(line is ''): continue
            if('group' in line):
                (group, division, compet, season) = _split_descriptor(line)
                num_round = line.split('round:')[1].split(',')[0]
                uidGroup = season+'_'+compet+'_'+division+'_'+group
                uidRound = uidGroup + '_'+str(num_round)
                values = _concat_round_values(uidRound, num_round, uidGroup)
                cursor.execute("INSERT INTO ROUNDS VALUES " + values)
                num_match = 0
            else:
                (actor1, score, actor2) = line.split('\t')
                if(actor1 in teams and actor2 in teams):
                    num_match += 1
                    num_board = 0
                    uidMatch = uidRound + '_' + str(num_match)
                    if score != "  -  ":
                        values = _concat_match_values(uidMatch, actor1, actor2, score, uidRound)
                        cursor.execute("INSERT INTO MATCHS VALUES " + values)
                else:
                    num_board += 1
                    values = _concat_game_values(actor1, actor2, num_board, score, uidMatch)
                    cursor.execute("INSERT INTO GAMES VALUES " + values)
        except:
            pass
    _close_and_commit(db)
