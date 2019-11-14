#!/usr/local/bin/casperjs

function get_element_options(selector) {
    html_info = casper.getElementInfo(selector).html;
    var options=[];
    html_info.split('</option>').forEach(function(option) {
        if(option.includes('value="') && !option.includes("Sélectionne")){
            options.push(option.split('value="')[1].split('">'));
        }
    });
    return options
}

function loop_over_divisions(divisions, compet_str){
    divisions.forEach(function(division) {
        casper.wait(20).then(function() {
            division_str = compet_str + ",division_id:" + division[0] + ",division_label:" + division[1];
            casper.echo(division_str);
            this.fillSelectors('form[id="aspnetForm"]', {
                'select[id="ctl00_ContentPlaceHolderMain_SelectDivision"]': division[0]
            }, false);
            casper.wait(20).then(function() {
                groups = get_element_options('select[id="ctl00_ContentPlaceHolderMain_SelectGroupe"]');
                for (var i=0; i<groups.length; i++) {
                    group_str = division_str + ",group_id:" + groups[i][0] + ",group_label:" + groups[i][1];
                    casper.echo(group_str);
                }
            });
        });
    });
}

function loop_over_competitions(competitions, season_str) {
    competitions.forEach(function(compet) {
        casper.wait(20).then(function() {
            compet_str = season_str + ",compet_id:" + compet[0] + ",compet_label:" + compet[1];
            casper.echo(compet_str);
            this.fillSelectors('form[id="aspnetForm"]', {
                'select[id="ctl00_ContentPlaceHolderMain_SelectCompetition"]': compet[0]
            }, false);
            casper.wait(20).then(function() {
                divisions = get_element_options('select[id="ctl00_ContentPlaceHolderMain_SelectDivision"]');
                loop_over_divisions(divisions, compet_str);
            });
        });
    });
}

var casper = require('casper').create();

// removing default options passed by the Python executable
casper.cli.drop("cli");
casper.cli.drop("casper-path");

// Start navigation
casper.start("http://www.echecs.asso.fr/Equipes.aspx");

casper.then(function() {
    var seasons = this.getElementsAttribute('a[class="lien_texte"]', 'id');
    seasons.forEach(function(id) {
        casper.wait(20).then(function() {
            var btn_text = casper.getElementInfo('a[id="' + id + '"]').text;
            var season_str = "season:" + btn_text;
            casper.echo(season_str);
            casper.click("a[id='" + id + "']");
            casper.wait(20).then(function() {
                var competitions = get_element_options('select[id="ctl00_ContentPlaceHolderMain_SelectCompetition"]');
                loop_over_competitions(competitions, season_str);
            });
        });
    });
});

casper.run();

