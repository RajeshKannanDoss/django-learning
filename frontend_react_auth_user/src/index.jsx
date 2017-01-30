import React, { Component } from 'react';
import { render } from 'react-dom';
// import routing components
import {Router, Route, browserHistory} from 'react-router';

// import custom components
import Settings from './common/settings/settings.component.jsx';
import MainContent from './common/main-content/main_content.component.jsx';
import Main from './common/main/main.component.jsx';
import CreateLeagueForm from './common/create/createleague.component.jsx';
import CreateTeamForm from './common/create/createteam.component.jsx';
import CreatePlayerForm from './common/create/createplayer.component.jsx';
import CreateTeamStatForm from './common/create/createteamstat.component.jsx';
import CreateMatchForm from './common/create/creatematch.component.jsx';

render(
    <Router history={browserHistory}>
        <Route component={Main}>
            <Route path='/fifa' component={MainContent} />
            <Route path="/fifa/settings" component={Settings} />
        </Route>
    </Router>,
    document.getElementById('root')
);

document.getElementById('close-form-button').addEventListener('click', function()
{
    this.parentElement.classList.remove('animation_from');
    this.parentElement.classList.add('animation_to');
});

document.getElementById('close-edit-button').addEventListener('click', function()
{
    this.parentElement.classList.remove('animation_from');
    this.parentElement.classList.add('animation_to');
});

var createLeagueOpenButton = document.getElementById('create-league-open-button');
var createTeamOpenButton = document.getElementById('create-team-open-button');
var createPlayerOpenButton = document.getElementById('create-player-open-button');
var createTeamStatOpenButton = document.getElementById('create-teamstat-open-button');
var createMatchOpenButton = document.getElementById('create-match-open-button');

createLeagueOpenButton.addEventListener('click', function(){
    document.getElementsByClassName('focus_button')[0].classList.remove('focus_button');
    createLeagueOpenButton.classList.add('focus_button');
    render(
        <CreateLeagueForm league='' />,
        document.getElementById('focus-form')
    );
});

createTeamOpenButton.addEventListener('click', function(){
    document.getElementsByClassName('focus_button')[0].classList.remove('focus_button');
    createTeamOpenButton.classList.add('focus_button');
    render(
        <CreateTeamForm />,
        document.getElementById('focus-form')
    );
});

createPlayerOpenButton.addEventListener('click', function(){
    document.getElementsByClassName('focus_button')[0].classList.remove('focus_button');
    createPlayerOpenButton.classList.add('focus_button');
    render(
        <CreatePlayerForm />,
        document.getElementById('focus-form')
    );
});

createTeamStatOpenButton.addEventListener('click', function(){
    document.getElementsByClassName('focus_button')[0].classList.remove('focus_button');
    createTeamStatOpenButton.classList.add('focus_button');
    render(
        <CreateTeamStatForm />,
        document.getElementById('focus-form')
    );
});

createMatchOpenButton.addEventListener('click', function(){
    document.getElementsByClassName('focus_button')[0].classList.remove('focus_button');
    createMatchOpenButton.classList.add('focus_button');
    render(
        <CreateMatchForm />,
        document.getElementById('focus-form')
    );
});

render(
    <CreateLeagueForm league='' />,
    document.getElementById('focus-form')
);
