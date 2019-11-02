#!/bin/bash

# TODO Struct db of seasons, compets, divisions and groups
# TODO Struct db of teams and games (v2 clubs and players)

# TODO Build db SCDG

# Loop over SCDG

compet=2
division=7
group=879
season=2019

[ ! -d "./results" ] && mkdir ./results
casperjs dump_teams.js --compet=$compet --division=$division --group=$group --season=$season | grep "^[1-9]\|group" > results/teams.tmp
casperjs dump_round_details.js --compet=$compet --division=$division --group=$group --season=$season | grep -v "^Comp\|^TypeError" > results/round_details.tmp

python3 parse_teams_to_db.py --file=results/teams.tmp --db=results/superffe.sqlite
python3 parse_round_details_to_db.py --file=results/round_details.tmp --db=results/superffe.sqlite
