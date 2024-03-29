import sqlite3

class DB:
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS SEASONS (labelSeason text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS COMPETITIONS (uNumCompetition text, idCompetition int, labelCompetition text, labelSeason text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS DIVISIONS (uNumDivision text, idDivision int, labelDivision text, uNumCompetition text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS GROUPS (uNumGroup text, idGroup int, labelGroup text, uNumDivision text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS TEAMS (labelTeam text, placeTeam int, pointsTeam int, j int, d int, p int, c int, uidGroup text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS ROUNDS (uidRound text, numRound int, uidGroup text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS MATCHS (uidMatch text, team1 text, team2 text, scoreMatch text, uidRound text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS GAMES (player1 text, elo1 int, player2 text, elo2 int, numBoard int, scoreGame text, uidMatch text)")

    def __del__(self):
        self.db.commit()
        self.db.close()

    def parse_groups(self, input_file):
        for line in open(input_file, 'r'):
            if(line[-1:] is '\n'): line = line[:-1]
            if "group_id:" in line:
                values = self._concat_group_values(line)
                self.cursor.execute("INSERT INTO GROUPS VALUES " + values)
            elif "division_id:" in line:
                values = self._concat_division_values(line)
                self.cursor.execute("INSERT INTO DIVISIONS VALUES " + values)
            elif "compet_id:" in line:
                values = self._concat_compet_values(line)
                self.cursor.execute("INSERT INTO COMPETITIONS VALUES " + values)
            elif "season:" in line:
                labelSeason = line.split(',')[0].split(':')[1]
                values = "('"+labelSeason+"')"
                self.cursor.execute("INSERT INTO SEASONS VALUES " + values)

    def parse_teams(self, input_file):
        (group, division, compet, season) = ("", "", "", "")
        for line in open(input_file, 'r'):
            if(line[-1:] is '\n'): line = line[:-1]
            if('group' in line):
                (group, division, compet, season) = self._split_descriptor(line)
                uidGroup = season+'_'+compet+'_'+division+'_'+group
            else:
                values = self._concat_team_values(line, uidGroup)
                self.cursor.execute("INSERT INTO TEAMS VALUES " + values)

    def parse_round_details(self, input_file):
        teams = self._get_team_labels()
        num_round = ""
        num_match = 0
        for line in open(input_file, 'r'):
            try:
                if(line[-1:] is '\n'): line = line[:-1]
                if(line[-1:] is '\t'): line = line[:-1]
                if(line is ''): continue
                if('group' in line):
                    (group, division, compet, season) = self._split_descriptor(line)
                    num_round = line.split('round:')[1].split(',')[0]
                    uidGroup = season+'_'+compet+'_'+division+'_'+group
                    uidRound = uidGroup+'_'+str(num_round)
                    values = self._concat_round_values(uidRound, num_round, uidGroup)
                    self.cursor.execute("INSERT INTO ROUNDS VALUES " + values)
                    num_match = 0
                else:
                    (actor1, score, actor2) = line.split('\t')
                    if(actor1 in teams and actor2 in teams):
                        num_match += 1
                        num_board = 0
                        uidMatch = uidRound + '_' + str(num_match)
                        if score != "  -  ":
                            values = self._concat_match_values(uidMatch, actor1, actor2, score, uidRound)
                            self.cursor.execute("INSERT INTO MATCHS VALUES " + values)
                    else:
                        num_board += 1
                        values = self._concat_game_values(actor1, actor2, num_board, score, uidMatch)
                        self.cursor.execute("INSERT INTO GAMES VALUES " + values)
            except:
                pass

    def _get_team_labels(self):
        teams = []
        for team_array in self.cursor.execute("SELECT labelTeam FROM TEAMS"):
            teams.append(team_array[0])
        return teams
    
    def _concat_group_values(self, line):
        labelSeason = line.split(',')[0].split(':')[1]
        idCompetition = line.split(',')[1].split(':')[1]
        idDivision = line.split(',')[3].split(':')[1]
        idGroup = line.split(',')[5].split(':')[1]
        labelGroup = line.split(',')[6].split(':')[1]
        uNumGroup = labelSeason + '_' + idCompetition + '_' + idDivision + '_' + idGroup
        uNumDivision = labelSeason + '_' + idCompetition + '_' + idDivision
        return "('" + uNumGroup + "'," + idGroup + ",'" + \
                labelGroup + "','" + uNumDivision + "')"
    
    def _concat_division_values(self, line):
        labelSeason = line.split(',')[0].split(':')[1]
        idCompetition = line.split(',')[1].split(':')[1]
        idDivision = line.split(',')[3].split(':')[1]
        labelDivision = line.split(',')[4].split(':')[1]
        uNumDivision = labelSeason + '_' + idCompetition + '_' + idDivision
        uNumCompetition = labelSeason + "_" + idCompetition
        return "('" + uNumDivision + "'," + idDivision + ",'" + \
                labelDivision + "','" + uNumCompetition + "')"

    def _concat_compet_values(self, line):
        idCompetition = line.split(',')[1].split(':')[1]
        labelCompetition = line.split(',')[2].split(':')[1]
        labelSeason = line.split(',')[0].split(':')[1]
        uNumCompetition = labelSeason + "_" + idCompetition
        return "('" + uNumCompetition + "'," + idCompetition + ",'" + \
                labelCompetition + "','" + labelSeason + "')"
                
    def _concat_game_values(self, actor1, actor2, board, score, uidMatch):
        (player1, elo1) = actor1.rsplit(' ', 1)
        (player2, elo2) = actor2.rsplit(' ', 1)
        return "('" + player1 + "'," + elo1 + ",'" + player2 + "'," + elo2 + \
                "," + str(board) + ",'" + score + "','" + uidMatch + "')"

    def _concat_match_values(self, uidMatch, actor1, actor2, score, num_round):
        return "('" + uidMatch + "','" + actor1 + "','" + actor2 + \
                "','" + score + "','" + num_round + "')"

    def _concat_team_values(self, line, group):
        (place, label, points, j, d, p, c) = line.split('\t')
        return "('" + label + "'," + place + "," + points + "," + j + \
                "," + d + "," + p + "," + c + ",'" + group + "')"

    def _concat_round_values(self, uidRound, num_round, uidGroup):
        return "('" + uidRound + "'," + num_round + ",'" + uidGroup + "')"

    def _split_descriptor(self, line):
        group = line.split('group:')[1].split(',')[0]
        division = line.split('division:')[1].split(',')[0]
        compet = line.split('compet:')[1].split(',')[0]
        season = line.split('season:')[1]
        return (group, division, compet, season)
       
