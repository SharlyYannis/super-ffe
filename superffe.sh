#!/bin/bash

[ ! -d "results" ] && mkdir results
[ -e "results/superffe.sqlite" ] && rm results/superffe.sqlite

echo -n "Extracting Seasons, Competitions, Divisions and Groups..."
#casperjs dump_groups.js | grep -v "TypeError" | sed "s/'/ /g" > results/groups.tmp
echo " OK!"

echo -n "Building DB with Seasons, Competitions, Divisions and Groups..."
python3 -c'from superffe import DB; db=DB("results/superffe.sqlite"); db.parse_groups("results/groups.tmp")'
echo " OK!"
sqlite3 results/superffe.sqlite "select labelSeason, idCompetition, idDivision, idGroup from (select * from divisions join competitions on divisions.uNumCompetition = competitions.uNumCompetition) as A join groups on A.uNumDivision = groups.uNumDivision" > results/loopable.tmp

while read line; do

    season=`echo "$line" | cut -f1 -d\|`
    compet=`echo "$line" | cut -f2 -d\|`
    division=`echo "$line" | cut -f3 -d\|`
    group=`echo "$line" | cut -f4 -d\|`

    echo $line    
    if [ $season != "Actuelle" ]
    then
        continue
    fi

    casperjs dump_teams.js --compet=$compet --division=$division --group=$group --season=$season | grep "^[1-9]\|group" > results/teams.tmp
    casperjs dump_round_details.js --compet=$compet --division=$division --group=$group --season=$season | grep -v "^Comp\|^TypeError" | sed "s/\xC2\xA0\|'/ /g" > results/round_details.tmp

    python3 -c'from superffe import DB; db=DB("results/superffe.sqlite"); db.parse_teams("results/teams.tmp"); db.parse_round_details("results/round_details.tmp")'

done <results/loopable.tmp


