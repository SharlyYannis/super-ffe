#!/usr/bin/env python3

import sqlite3
from argparse import RawTextHelpFormatter, ArgumentParser

def create_argparser():
    argparser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    argparser.add_argument('--file', required=True,
            help='Input file of plain text team rankings')
    argparser.add_argument('--db', required=True,
            help='Output db')
    return argparser



argparser = create_argparser()
args = vars(argparser.parse_args())

db = sqlite3.connect(args['db'])
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS equipes (nom text, place int, points int, j int, d int, p int, c int, groupe int, division int, compet int, saison text)")

filename = args['file']
f = open(filename, 'r')
(group, division, compet, season) = ("", "", "", "")
for line in f:
    if(line[-1:] is '\n'): line = line[:-1]
    if('group' in line):
        group = line.split('group:')[1].split(',')[0]
        division = line.split('division:')[1].split(',')[0]
        compet = line.split('compet:')[1].split(',')[0]
        season = line.split('season:')[1]
    else:
        (place, name, points, j, d, p, c) = line.split('\t')
        values= "('" + name + \
                "'," + place + \
                "," + points + \
                "," + j + \
                "," + d + \
                "," + p + \
                "," + c + \
                "," + group + \
                "," + division + \
                "," + compet + \
                ",'" + season + "')"
        cursor.execute("INSERT INTO equipes VALUES " + values)
        
db.commit()
db.close()
