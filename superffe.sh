#!/bin/bash

compet=2
division=7
group=879
season=2019

mkdir results
./get_teams.js --compet=$compet --division=$division --group=$group --season=$season | grep ^[1-9] > results/teams.tmp
./get_round_details.js --compet=$compet --division=$division --group=$group --season=$season | grep -v "^Comp\|^TypeError" > results/round_details.tmp



