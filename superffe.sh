#!/bin/bash

# TODO Build db of seasons, compets, divisions and groups

# Loop over SCDG

compet=2
division=7
group=879
season='Actuelle'

[ ! -d "results" ] && mkdir results
[ -e "results/superffe.sqlite" ] && rm results/superffe.sqlite

echo -n "Extracting Seasons, Competitions, Divisions and Groups..."
#casperjs dump_groups.js | grep -v "TypeError" | sed "s/'/ /g" > results/groups.tmp
echo " OK!"

echo -n "Building DB with Seasons, Competitions, Divisions and Groups..."
python3 -c'from superffe import DB; db=DB("results/superffe.sqlite"); db.parse_groups("results/groups.tmp")'
echo " OK!"

echo -n "Extracting Teams from group $group..."
casperjs dump_teams.js --compet=$compet --division=$division --group=$group --season=$season | grep "^[1-9]\|group" > results/teams.tmp
echo " OK!"

echo -n "Extracting round details from group $group..."
casperjs dump_round_details.js --compet=$compet --division=$division --group=$group --season=$season | grep -v "^Comp\|^TypeError" | sed "s/\xC2\xA0\|'/ /g" > results/round_details.tmp
echo " OK!"

echo -n "Adding teams and round details to DB for group $group..."
python3 -c'from superffe import DB; db=DB("results/superffe.sqlite"); db.parse_teams("results/teams.tmp"); db.parse_round_details("results/round_details.tmp")'
echo " OK!"
