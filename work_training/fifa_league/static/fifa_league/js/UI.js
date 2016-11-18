var UI = {
    init: function () {
        var leagueMenuButton = $("#add-league-menu-button");
        var matchMenuButton = $("#add-match-menu-button");

        var leagueMenu = $("#add-league-menu");
        var matchMenu = $("#add-match-menu");

        var closeButton = $(".close");

        var createLeagueForm = $("#create-league-form");
        var createMatchForm = $("#create-match-form");

        // Menus open
        // START
        leagueMenuButton.on("click", function(){
            leagueMenu.fadeIn(250);
        })

        matchMenuButton.on("click", function(){
            matchMenu.fadeIn(250);
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
                    alert(response);
                })
                .fail(function (response) {
                    alert(response.responseText);
                })
            })
        // END

        // get all teams
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
                    console.log(response);
                })
        })
        // END

        // create match
        // START
         createMatchForm.on("submit", function(event)
            {
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
                    console(response);
                })
                .fail(function (response) {
                    console(response);
                })
            })
        // END
    }
}
