var UI = {
    init: function () {
        var leagueMenuButton = $("#add-league-menu-button");
        var matchMenuButton = $("#add-match-menu-button");
        var teamMenuButton = $("#add-team-menu-button");
        var playerMenuButton = $("#add-player-menu-button");
        var teamToLeagueMenuButton = $("#add-team-to-league-menu-button");

        var leagueMenu = $("#add-league-menu");
        var matchMenu = $("#add-match-menu");
        var teamMenu = $("#add-team-menu");
        var playerMenu = $("#add-player-menu");
        var teamToLeagueMenu = $("#add-team-to-league-menu");

        var closeButton = $(".close");

        var createLeagueForm = $("#create-league-form");
        var createMatchForm = $("#create-match-form");
        var createTeamForm = $("#create-team-form");
        var createPlayerForm = $("#create-player-form");
        var createTeamToLeagueForm = $("#create-team-to-league-form");

        // showAlert
        // START
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
        // END

        // Menus open
        // START
        leagueMenuButton.on("click", function(){
            leagueMenu.fadeIn(250);
        })

        matchMenuButton.on("click", function(){
            matchMenu.fadeIn(250);
        })

        teamMenuButton.on("click", function(){
            teamMenu.fadeIn(250);
        })

        playerMenuButton.on("click", function(){
            get_all_teams("player-team-form");
            playerMenu.fadeIn(250);
        })

        teamToLeagueMenuButton.on("click", function(){
            get_all_teams("team-to-league-team-form");
            teamToLeagueMenu.fadeIn(250);
        })
        // END

        // close menus
        // START
            closeButton.on("click", function()
            {
                $(this).parent().fadeOut(250);
            })
        // END

        // create league
        // START
            createLeagueForm.on("submit", function(event)
            {
                event.preventDefault();
                var obj = {
                    name: $("#league-name-form").val(),
                    shortcut: $("#league-shortcut-form").val(),
                }
                Ajax.send(obj, "/fifa/create_league/")
                .done(function (response) {
                    showAlert(response);
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
            })
        // END

        // first get all teams request | need refactory
        // START
         var obj = {
                    action: "get_teams_list_from_league",
                    league_shortcut: $("#match-league-form").val(),
                }
                Ajax.send(obj, "/fifa/get_data/")
                .done(function (response) {
                   teams_names_list = response['teams_names']
                   $("#match-home-form").empty();
                   $("#match-guest-form").empty();
                   for(i=0; i < teams_names_list.length; i++)
                   {
                   new_option = $("<option>");
                   new_option.attr("value", teams_names_list[i]);
                   new_option.html(teams_names_list[i]);
                   $("#match-home-form").append(new_option);

                   new_option = $("<option>");
                   new_option.attr("value", teams_names_list[i]);
                   new_option.html(teams_names_list[i]);

                   $("#match-guest-form").append(new_option);
                   }
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
        // END

        // get all teams for league
        // START
        $("#match-league-form").on("change", function(){
                var obj = {
                    action: "get_teams_list_from_league",
                    league_shortcut: $("#match-league-form").val(),
                }
                Ajax.send(obj, "/fifa/get_data/")
                .done(function (response) {
                   teams_names_list = response['teams_names']
                   $("#match-home-form").empty();
                   $("#match-guest-form").empty();
                   for(i=0; i < teams_names_list.length; i++)
                   {
                   new_option = $("<option>");
                   new_option.attr("value", teams_names_list[i]);
                   new_option.html(teams_names_list[i]);
                   $("#match-home-form").append(new_option);

                   new_option = $("<option>");
                   new_option.attr("value", teams_names_list[i]);
                   new_option.html(teams_names_list[i]);

                   $("#match-guest-form").append(new_option);
                   }
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
        })
        // END

        // create match
        // START
         createMatchForm.on("submit", function(event){
                event.preventDefault();
                var obj = {
                    league: $("#match-league-form").val(),
                    home_team: $("#match-home-form").val(),
                    guest_team:$("#match-guest-form").val(),
                    home_score:$("#match-home-score-form").val(),
                    guest_score: $("#match-guest-score-form").val(),
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
                    team_name: $("#team-name-form").val(),
                    team_shortcut: $("#team-shortcut-form").val(),
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
                    player_name: $("#player-name-form").val(),
                    player_age: $("#player-age-form").val(),
                    player_team: $("#player-team-form").val(),
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

        // get all teams (need to refactory in future)
        // START
        function get_all_teams(id){
                element = $("#" + id)
                var obj = {
                    action: "get_teams_list",
                    team: element.val(),
                }
                Ajax.send(obj, "/fifa/get_data/")
                .done(function (response) {
                   teams_names_list = response['teams_names']
                   element.empty();
                   for(i=0; i < teams_names_list.length; i++)
                   {
                   new_option = $("<option>");
                   new_option.attr("value", teams_names_list[i]);
                   new_option.html(teams_names_list[i]);

                   element.append(new_option);
                   }
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
        }
        // END

        // add team to league
        // START
        createTeamToLeagueForm.on("submit", function(event)
            {
                event.preventDefault();
                var obj = {
                    team_name: $("#team-to-league-team-form").val(),
                    league_name: $("#team-to-league-league-form").val(),
                }
                Ajax.send(obj, "/fifa/add_team_to_league/")
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
