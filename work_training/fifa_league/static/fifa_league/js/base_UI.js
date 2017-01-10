// AJAX functions
var Ajax={send:function(a,b,c){return $.ajax({type:"POST",url:b,data:a,dataType:c})},sendGET:function(a,b){return $.ajax({type:"GET",url:a,dataType:b})}};$(function(){function a(a){var b=null;if(document.cookie&&""!=document.cookie)for(var c=document.cookie.split(";"),d=0;d<c.length;d++){var e=jQuery.trim(c[d]);if(e.substring(0,a.length+1)==a+"="){b=decodeURIComponent(e.substring(a.length+1));break}}return b}function c(a){return/^(GET|HEAD|OPTIONS|TRACE)$/.test(a)}function d(a){var b=document.location.host,c=document.location.protocol,d="//"+b,e=c+d;return a==e||a.slice(0,e.length+1)==e+"/"||a==d||a.slice(0,d.length+1)==d+"/"||!/^(\/\/|http:|https:).*/.test(a)}var b=a("csrftoken");$.ajaxSetup({beforeSend:function(a,e){!c(e.type)&&d(e.url)&&a.setRequestHeader("X-CSRFToken",b)}})});

var base_UI = {
    init: function ()
    {
        // buttons set
        var closeButton = $(".close");
        var userFormDivButton = $("#user-form-div-button");
        var userCreateFormSubmitButton = $("#user-create-submit-button");
        var userLoginFormSubmitButton = $("#user-login-submit-button");
        var userOpenCreateFormButton = $("#user-signup-open-button");
        var userOpenLoginFormButton = $("#user-login-open-button");

        // form div set
        var userFormDiv = $("#user-form-div");

        // form variables set
        var createUserForm = $("#user-registration-form");
        var loginUserForm = $("#user-login-form");

        // menus sequence setup
        $(".menus_choose_buttons_div div:first").addClass('focus_button');
        $(".menus_forms_div form:first").addClass('focus_form');

        // showAlert
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

        // open forms menu to log or signup user
        userFormDivButton.on("click", function()
        {
           userFormDiv.fadeIn(250);
        });

        // open form to create user
        userOpenCreateFormButton.on("click", function()
        {
            userOpenCreateFormButton.addClass('focus_button');
            userOpenLoginFormButton.removeClass('focus_button');
            loginUserForm.removeClass('focus_form');
            createUserForm.addClass('focus_form');
        });

        // open form to login user
        userOpenLoginFormButton.on("click", function()
        {
            userOpenLoginFormButton.addClass('focus_button');
            userOpenCreateFormButton.removeClass('focus_button');
            createUserForm.removeClass('focus_form');
            loginUserForm.addClass('focus_form');
        });

        // close menu button
        closeButton.on("click", function()
        {
            $(this).parent().fadeOut(250);
        })

        // create user form
        // START
        createUserForm.on("submit", function(event)
        {
            event.preventDefault();
            var obj = {
                    username: $("#user-registration-form input[name=username]").val(),
                    email: $("#user-registration-form input[name=email]").val(),
                    password: $("#user-registration-form input[name=password]").val(),
            }
             Ajax.send(obj, "/fifa/create_user/")
                    .done(function (response) {
                        location.reload(true);
                    })
                    .fail(function (response) {
                        showAlert(response.responseText);
                    })

        })
        // END

        // log in user form
        // START
        loginUserForm.on("submit", function(event)
        {
            event.preventDefault();
            var obj = {
                    username: $("#user-login-form input[name=username]").val(),
                    password: $("#user-login-form input[name=password]").val()
            }
             Ajax.send(obj, "/fifa/login_user/")
                    .done(function (response) {
                        location.reload(true);
                    })
                    .fail(function (response) {
                        showAlert(response.responseText);
                    })

        })
        // END
    }
}