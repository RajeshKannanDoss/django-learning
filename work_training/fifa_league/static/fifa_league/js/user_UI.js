// AJAX functions
var Ajax={send:function(a,b,c){return $.ajax({type:"POST",url:b,data:a,dataType:c})},sendGET:function(a,b){return $.ajax({type:"GET",url:a,dataType:b})}};$(function(){function a(a){var b=null;if(document.cookie&&""!=document.cookie)for(var c=document.cookie.split(";"),d=0;d<c.length;d++){var e=jQuery.trim(c[d]);if(e.substring(0,a.length+1)==a+"="){b=decodeURIComponent(e.substring(a.length+1));break}}return b}function c(a){return/^(GET|HEAD|OPTIONS|TRACE)$/.test(a)}function d(a){var b=document.location.host,c=document.location.protocol,d="//"+b,e=c+d;return a==e||a.slice(0,e.length+1)==e+"/"||a==d||a.slice(0,d.length+1)==d+"/"||!/^(\/\/|http:|https:).*/.test(a)}var b=a("csrftoken");$.ajaxSetup({beforeSend:function(a,e){!c(e.type)&&d(e.url)&&a.setRequestHeader("X-CSRFToken",b)}})});

var user_UI = {
    init: function ()
    {
        var menusOpenButton = $("#menus-open-button");
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
        var changePasswordForm = $("#user-change-password-form");
        var changeEmailForm = $("#user-change-email-form");

        var leagueLogoFileInput = $('#create-league-form input[name=logo]');

        // menus sequence set up
        // TODO: Refactor this part of code
        $(".menus_choose_buttons_div div:first").addClass('focus_button');
        $(".menus_forms_div form:first").addClass('focus_form');

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
            $(".menu_form").removeClass("focus_form");
            $(".focus_button").removeClass('focus_button')
            createLeagueForm.addClass("focus_form");
            leagueCreateFormOpenButton.addClass('focus_button');
        });

        teamCreateFormOpenButton.on("click", function(){
            $(".menu_form").removeClass("focus_form");
            $(".focus_button").removeClass('focus_button');
            createTeamForm.addClass("focus_form");
            teamCreateFormOpenButton.addClass('focus_button');
        });

        playerCreateFormOpenButton.on("click", function(){
            $(".menu_form").removeClass("focus_form");
            $(".focus_button").removeClass('focus_button');
            createPlayerForm.addClass("focus_form");
            playerCreateFormOpenButton.addClass('focus_button');
        });

        teamstatCreateFormOpenButton.on("click", function(){
            $(".menu_form").removeClass("focus_form");
            $(".focus_button").removeClass('focus_button');
            createTeamStatForm.addClass("focus_form");
            teamstatCreateFormOpenButton.addClass('focus_button');
        });

        matchCreateFormOpenButton.on("click", function()
        {
            $(".menu_form").removeClass('focus_form');
            $(".focus_button").removeClass('focus_button');
            createMatchForm.addClass("focus_form");
            matchCreateFormOpenButton.addClass('focus_button');
        })

        // open list of menus 'Add new item'
        menusOpenButton.on("click", function()
        {
            menusDiv.fadeIn(250);
        });
        // END


        // create league
        // START
        leagueLogoFileInput.fileupload({
            replaceFileInput: false,
            add: function (e, data) {
                createLeagueForm.off('submit').on("submit", function(event)
                {
                    event.preventDefault();
                    url = createLeagueForm.attr('action');
                    data.url = url;
                    data.formData = {
                        name: $("#create-league-form input[name=name]").val(),
                        shortcut: $("#create-league-form input[name=shortcut]").val(),
                        short_description: $("#create-league-form input[name=short_description]").val(),
                        full_description: $("#create-league-form textarea[name=full_description]").val(),
                    }
                    data.submit();
                });
            },
            done: function (e, data) {
                showAlert(data._response.result);
            },
            fail: function (e, data)
            {
                showAlert(data._response.jqXHR.responseText);
            }
        });

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

        changePasswordForm.on("submit", function(event)
        {
            event.preventDefault();
            url = changePasswordForm.attr('action');
            var obj = {
                    old_password: $("#user-change-password-form input[name=old_password]").val(),
                    new_password1: $("#user-change-password-form input[name=new_password1]").val(),
                    new_password2: $("#user-change-password-form input[name=new_password2]").val(),
                }
                Ajax.send(obj, url)
                .done(function (response) {
                    showAlert(response);
                    $(':input','#user-change-password-form')
                        .removeAttr('checked')
                        .removeAttr('selected')
                        .not(':button, :submit, :reset, :hidden, :radio, :checkbox')
                        .val('');
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
        })

        changeEmailForm.on("submit", function(event)
        {
            event.preventDefault();
            url = changeEmailForm.attr('action');
            var obj = {
                    new_email: $("#user-change-email-form input[name=new_email]").val()
                }
                Ajax.send(obj, url)
                .done(function (response) {
                    showAlert(response);
                    $(':input','#user-change-email-form')
                        .removeAttr('checked')
                        .removeAttr('selected')
                        .not(':button, :submit, :reset, :hidden, :radio, :checkbox')
                        .val('');
                })
                .fail(function (response) {
                    showAlert(response.responseText);
                })
        })

        $("#avatar-upload-button").on("click", function()
        {
            $("#avatarupload").click();
        });

        $("#avatarupload").fileupload({
            dataType: 'json',
            done: function (e, data) {
                if(data.result.is_valid)
                {
                    $('#avatar-img').attr('src', data.result.url);
                    $('.user_avatar').attr('src', data.result.url);
                    $("#avatar-message").addClass('message_ok');
                    $('#avatar-message').html(data.result.message);
                } else
                {
                    $("#avatar-message").addClass('message_error');
                    $('#avatar-message').html(data.result.message);
                }
            }
        })
    }
}