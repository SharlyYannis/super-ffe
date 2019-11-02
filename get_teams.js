#!/usr/local/bin/casperjs

var casper = require('casper').create();

// removing default options passed by the Python executable
casper.cli.drop("cli");
casper.cli.drop("casper-path");
// display help
if (!casper.cli.has("compet") || !casper.cli.has("division") || !casper.cli.has("group")) {
    casper.echo("Usage: $ ./get_games.js --compet=<COMPET_ID> --division=<DIVISION_ID --group=<GROUP_ID> [--season=<SAISON>]").exit();
}

var compet = casper.cli.get("compet").toString();
var division = casper.cli.get("division").toString();
var group = casper.cli.get("group").toString();
var season = "Actuelle";
if (casper.cli.has("season")) {
    season = casper.cli.get("season").toString();
}


// Start navigation
casper.start("http://www.echecs.asso.fr/Equipes.aspx");

// Select season
casper.then(function() {
    var btn_ids = this.getElementsAttribute('a[class="lien_texte"]', 'id');
    btn_ids.forEach(function(id) {
        var btn_text = casper.getElementInfo('a[id="' + id + '"]').text;
        if(btn_text === season) {
            casper.click("a[id='" + id + "']");
        }
    });
});

// Select competition
casper.wait(20).then(function() {
    this.fillSelectors('form[id="aspnetForm"]', {
        'select[id="ctl00_ContentPlaceHolderMain_SelectCompetition"]': compet
    }, false);
});

// Select division
casper.wait(20).then(function() {
    this.fillSelectors('form[id="aspnetForm"]', {
        'select[id="ctl00_ContentPlaceHolderMain_SelectDivision"]': division
    }, false);
});

// Select group
casper.wait(20).then(function() {
    this.fillSelectors('form[id="aspnetForm"]', {
        'select[id="ctl00_ContentPlaceHolderMain_SelectGroupe"]': group
    }, false);
});

// Dump team rankings
casper.then(function() {
    var plain_text = casper.getPlainText();
    casper.echo(plain_text.split("\n\n")[4].split("Imprimer")[0]);
});

casper.run();
