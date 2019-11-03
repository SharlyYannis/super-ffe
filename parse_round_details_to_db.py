#!/usr/bin/env python3

import sqlite3
from argparse import RawTextHelpFormatter, ArgumentParser

def create_argparser():
    argparser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    argparser.add_argument('--file', required=True,
            help='Input file of plain text round details')
    argparser.add_argument('--db', required=True,
            help='Output db')
    return argparser



argparser = create_argparser()
args = vars(argparser.parse_args())

db = sqlite3.connect(args['db'])
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS matchs (club1 text, club2 text, score text, num int, ronde int, groupe int, division int, compet int, saison text)")
cursor.execute("CREATE TABLE IF NOT EXISTS parties (joueur1 text, elo1 int, joueur2 text, elo2 int, score text, match_num int, ronde int, groupe int, division int, compet int, saison text)")

teams = []
for team_array in cursor.execute("SELECT nom FROM equipes"):
    teams.append(team_array[0])

filename = args['file']
f = open(filename, 'r')
num_match = 0
(ronde, group, division, compet, season) = ("", "", "", "", "")
for line in f:
    if(line[-1:] is '\n'): line = line[:-1]
    if(line[-1:] is '\t'): line = line[:-1]
    if(line is ''): continue
    if('group' in line):
        ronde = line.split('round:')[1].split(',')[0]
        group = line.split('group:')[1].split(',')[0]
        division = line.split('division:')[1].split(',')[0]
        compet = line.split('compet:')[1].split(',')[0]
        season = line.split('season:')[1]
        num_match = 0
    else:
        try:
            (actor1, score, actor2) = line.split('\t')
            if(actor1 in teams and actor2 in teams):
                num_match += 1
                values= "('" + actor1 + \
                        "','" + actor2 + \
                        "','" + score + \
                        "'," + str(num_match) + \
                        "," + ronde + \
                        "," + group + \
                        "," + division + \
                        "," + compet + \
                        ",'" + season + "')"
                cursor.execute("INSERT INTO matchs VALUES " + values)
            else:
                (player1, elo1) = actor1.rsplit(' ', 1)
                (player2, elo2) = actor2.rsplit(' ', 1)
                values= "('" + player1 + \
                        "'," + elo1 + \
                        ",'" + player2 + \
                        "'," + elo2 + \
                        ",'" + score + \
                        "'," + str(num_match) + \
                        "," + ronde + \
                        "," + group + \
                        "," + division + \
                        "," + compet + \
                        ",'" + season + "')"
                cursor.execute("INSERT INTO parties VALUES " + values)
        except: pass

db.commit()
db.close()
