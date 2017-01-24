import GuestProfilePresentation from './common/main/guestprofile.component.jsx';
import SignUpForm from './common/forms/signup.component.jsx';
import LoginForm from './common/forms/login.component.jsx';
import LeaguesList from './common/main-content/leagues.component.jsx';
import ReactDOM from 'react-dom';
import React, { Component } from 'react';

ReactDOM.render(
  <GuestProfilePresentation />,
  document.getElementById('profile-div')
);

ReactDOM.render(
    <SignUpForm />,
    document.getElementById('user-signup-form-div')
);

ReactDOM.render(
    <LoginForm />,
    document.getElementById('user-login-form-div')
);

ReactDOM.render(
    <LeaguesList />,
    document.getElementById('leagues-list-div')
);

document.getElementById('close-form-button').addEventListener('click', function()
{
    this.parentElement.classList.remove('animation_from');
    this.parentElement.classList.add('animation_to');
});

var userSignUpOpenButton = document.getElementById('user-signup-open-button');
var userLoginOpenButton = document.getElementById('user-login-open-button');

var userSignUpForm = document.getElementById('user-signup-form-div');
var userLoginForm = document.getElementById('user-login-form-div');

userLoginOpenButton.addEventListener('click', function(){
    userLoginForm.classList.add('focus_form');
    userLoginOpenButton.classList.add('focus_button');
    userSignUpForm.classList.remove('focus_form');
    userSignUpOpenButton.classList.remove('focus_button');
});

userSignUpOpenButton.addEventListener('click', function(){
    userLoginForm.classList.remove('focus_form');
    userLoginOpenButton.classList.remove('focus_button');
    userSignUpForm.classList.add('focus_form');
    userSignUpOpenButton.classList.add('focus_button');
});
