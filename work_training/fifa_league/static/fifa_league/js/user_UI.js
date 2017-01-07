// AJAX functions
var Ajax={send:function(a,b,c){return $.ajax({type:"POST",url:b,data:a,dataType:c})},sendGET:function(a,b){return $.ajax({type:"GET",url:a,dataType:b})}};$(function(){function a(a){var b=null;if(document.cookie&&""!=document.cookie)for(var c=document.cookie.split(";"),d=0;d<c.length;d++){var e=jQuery.trim(c[d]);if(e.substring(0,a.length+1)==a+"="){b=decodeURIComponent(e.substring(a.length+1));break}}return b}function c(a){return/^(GET|HEAD|OPTIONS|TRACE)$/.test(a)}function d(a){var b=document.location.host,c=document.location.protocol,d="//"+b,e=c+d;return a==e||a.slice(0,e.length+1)==e+"/"||a==d||a.slice(0,d.length+1)==d+"/"||!/^(\/\/|http:|https:).*/.test(a)}var b=a("csrftoken");$.ajaxSetup({beforeSend:function(a,e){!c(e.type)&&d(e.url)&&a.setRequestHeader("X-CSRFToken",b)}})});

var user_UI = {
    init: function ()
    {
        var menusOpenButton = $("#menus-open-button");
        var userCreateFormSubmitButton = $("#user-create-submit-button");
        var userLoginFormSubmitButton = $("#user-login-submit-button");
        var userOpenCreateFormButton = $("#user-signup-open-button");
        var userOpenLoginFormButton = $("#user-login-open-button");

        var leagueCreateFormOpenButton = $("#league-create-form-open-button");
        var teamCreateFormOpenButton = $("#team-create-form-open-button");
        var playerCreateFormOpenButton = $("#player-create-form-open-button");
        var teamstatCreateFormOpenButton = $("#teamstat-create-form-open-button");
        var matchCreateFormOpenButton = $("#match-create-form-open-button");

        var leagueMenu = $("#add-league-menu");
        var matchMenu = $("#add-match-menu");
        var teamMenu = $("#add-team-menu");
        var playerMenu = $("#add-player-menu");
        var teamToLeagueMenu = $("#add-team-to-league-menu");
        var menusDiv = $("#fullscreen-add-menus-div");

        var closeButton = $(".close");

        var createLeagueForm = $("#create-league-form");
        var createMatchForm = $("#create-match-form");
        var createTeamForm = $("#create-team-form");
        var createPlayerForm = $("#create-player-form");
        var createTeamStatForm = $("#create-teamstat-form");

        // showAlert function
        var alertDiv = $("#alert-div");
        var alertDivMes = $("#alert-div-mes");
        function showAlert(mes)
        {
            if(mes == "")
            {
                mes = "[!] Unknown error";
            }
            alertDivMes.html(mes);
            alertDiv.fadeIn(100).delay(2000).fadeOut(500);
        }

        // close menu
        closeButton.on("click", function()
        {
            $(this).parent().fadeOut(250);
        })

        // Menus open
        // START
        leagueCreateFormOpenButton.on("click", function(){
            $(".menus_form").removeClass("focus_form");
            createLeagueForm.addClass("focus_form");
        });

        teamCreateFormOpenButton.on("click", function(){
            $(".menus_form").removeClass("focus_form");
            createTeamForm.addClass("focus_form");
        });

        playerCreateFormOpenButton.on("click", function(){
            $(".menus_form").removeClass("focus_form");
            createPlayerForm.addClass("focus_form");
        });

        teamstatCreateFormOpenButton.on("click", function(){
            $(".menus_form").removeClass("focus_form");
            createTeamStatForm.addClass("focus_form");
        });

        matchCreateFormOpenButton.on("click", function()
        {
            $(".menus_form").removeClass('focus_form');
            createMatchForm.addClass("focus_form");
        })

        // open list of menus 'Add new item'
        menusOpenButton.on("click", function()
        {
            menusDiv.fadeIn(250);
        });
        // END

        // create league
        // START
            createLeagueForm.on("submit", function(event)
            {
                event.preventDefault();
                var obj = {
                    name: $("#create-league-form input[name=name]").val(),
                    shortcut: $("#create-league-form input[name=shortcut]").val(),
                }
                Ajax.send(obj, "/fifa/create_league/")
                .done(function (response) {
                    showAlert(response);
                    if($("#leagues-list") != undefined)
                    {
                        $("#leagues-list").empty();
                    Ajax.sendGET("/fifa/api/leagues/")
                    .done(function (response) {
                        $.each(response, function(key, value) {
                            $("#leagues-list")
                                .append($("<li></li>")
                                .append($("<a></a>").attr("href", value['shortcut']).text(value['name'])));
                    });
                    })
                    .fail(function (response) {
                        showAlert(response.responseText);
                    })
                    }
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
            })
        // END

        // function to get all teams related to specific League
        // START
        function get_all_teams_by_league(league_shortcut)
        {
            Ajax.sendGET("/fifa/api/teams/get_teams_from_league/" + league_shortcut + "/")
                .done(function (response) {
                    matchSelectTeamHome = $("#create-match-form select[name=team_home]").empty();
                    matchSelectTeamGuest = $("#create-match-form select[name=team_guest]").empty();

                    $.each(response, function(key, value) {
                        matchSelectTeamHome
                            .append($("<option></option>")
                            .attr("value", value['shortcut']).text(value['name']));
                    });
                    $.each(response, function(key, value) {
                        matchSelectTeamGuest
                            .append($("<option></option>")
                            .attr("value", value['shortcut']).text(value['name']));
                    });
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
         }


        // END

        // startup set of options for match create
        league_shortcut = $("#create-match-form select[name=league]").val();
        get_all_teams_by_league(league_shortcut)

        // get all teams for league
        // START
        $("#create-match-form select[name=league]").on("change", function(){
                league_shortcut = $("#create-match-form select[name=league]").val();
                get_all_teams_by_league(league_shortcut)
        })
        // END

        // create match
        // START
         createMatchForm.on("submit", function(event){
                event.preventDefault();
                var obj = {
                    league: $("#create-match-form select[name=league]").val(),
                    team_home: $("#create-match-form select[name=team_home]").val(),
                    team_guest: $("#create-match-form select[name=team_guest]").val(),
                    team_home_goals: $("#create-match-form input[name=team_home_goals]").val(),
                    team_guest_goals: $("#create-match-form  input[name=team_guest_goals]").val(),
                }
                Ajax.send(obj, "/fifa/create_match/")
                .done(function (response) {
                    showAlert(response);
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
            })
        // END

        // create team
        // START
        createTeamForm.on("submit", function(event)
            {
                event.preventDefault();
                var obj = {
                    name: $("#create-team-form input[name=name]").val(),
                    shortcut: $("#create-team-form input[name=shortcut]").val(),
                }
                Ajax.send(obj, "/fifa/create_team/")
                .done(function (response) {
                    showAlert(response);
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
            })
        // END

        // create player
        // START
        createPlayerForm.on("submit", function(event)
            {
                event.preventDefault();
                var obj = {
                    name: $("#create-player-form input[name=name]").val(),
                    age: $("#create-player-form input[name=age]").val(),
                    team: $("#create-player-form select[name=team]").val(),
                }
                Ajax.send(obj, "/fifa/create_player/")
                .done(function (response) {
                    showAlert(response);
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
            })
        // END

        // START
        function get_all_teams(id){
                element = $("#" + id)
                Ajax.sendGET("/fifa/api/teams/")
                .done(function (response) {
                    $.each(response, function(key, value) {
                        element
                            .append($("<option></option>")
                            .attr("value", value['shortcut']).text(value['name']));
                    });
                })
                .fail(function (response) {
                    console.log(response.responseText);
                })
        }
        // END

        // add team to league | create teamstat
        // START
        createTeamStatForm.on("submit", function(event)
            {
                event.preventDefault();
                var obj = {
                    team: $("#create-teamstat-form select[name=team]").val(),
                    league: $("#create-teamstat-form select[name=league]").val(),
                }
                Ajax.send(obj, "/fifa/create_teamstat/")
                .done(function (response) {
                    showAlert(response);
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
            })
        // END
    }
}