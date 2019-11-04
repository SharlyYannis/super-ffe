#!/bin/bash

# TODO Build db of seasons, compets, divisions and groups

# Loop over SCDG

compet=2
division=7
group=879
season=2019

[ ! -d "results" ] && mkdir results
[ -e "results/superffe.sqlite" ] && rm results/superffe.sqlite

#casperjs dump_teams.js --compet=$compet --division=$division --group=$group --season=$season | grep "^[1-9]\|group" > results/teams.tmp

#casperjs dump_round_details.js --compet=$compet --division=$division --group=$group --season=$season | grep -v "^Comp\|^TypeError" | sed 's/\xC2\xA0/ /g' > results/round_details.tmp

python3 -c'from db_superffe import parse_teams; parse_teams("results/teams.tmp", "results/superffe.sqlite")'
sqlite3 results/superffe.sqlite "SELECT labelTeam FROM TEAMS"

python3 -c'from db_superffe import parse_round_details; parse_round_details("results/round_details.tmp", "results/superffe.sqlite")'
