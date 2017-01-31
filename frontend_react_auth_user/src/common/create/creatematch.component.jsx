import React, { Component } from 'react';
import { sendURLEncodedForm } from '../ajax.jsx';
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';
import axios from 'axios';
import ReactDOM from 'react-dom';
var qs = require('qs');

class CreateMatchForm extends Component
{
    constructor(props)
    {
        super(props);
        this.url = '/fifa/api/match/';
        this.state = {team_home:'', team_guest: '', league:'',
            team_list: [], league_list: [], team_home_goals: '',
            team_guest_goals: ''};
        this.handleTeamHome = this.handleTeamHome.bind(this);
        this.handleLeague = this.handleLeague.bind(this);
        this.handleTeamGuest = this.handleTeamGuest.bind(this);
        this.handleTeamGuestGoals = this.handleTeamGuestGoals.bind(this);
        this.handleTeamHomeGoals = this.handleTeamHomeGoals.bind(this);
    }

    update_team_list()
    {
        axios.get('/fifa/api/leagues/' + this.state.league + '/get_teams/')
            .then(res => {
                const team_list = res.data;
                this.setState({ team_list });
                this.setState({
                    team_home: team_list[0]['pk'],
                    team_guest: team_list[0]['pk']
                })
        });
    }

    componentDidMount() {
        axios.get('/fifa/api/leagues/')
            .then(res => {
                const league_list = res.data;
                this.setState({ league_list });
                this.setState({league: league_list[0]['pk']},
                function()
                {
                    this.update_team_list();
                });
        });
    }

    _handleSubmit(e)
    {
        e.preventDefault();
        var form = this;
        sendURLEncodedForm.post(this.url, qs.stringify({
            team_home: this.state.team_home,
            team_guest: this.state.team_guest,
            team_home_goals: this.state.team_home_goals,
            team_guest_goals: this.state.team_guest_goals,
            league: this.state.league
        }))
        .then(function (response) {
            showSuccess(response.data);
            form.setState({
                team_home_goals: '',
                team_guest_goals: ''
            });
        })
        .catch(function (error) {
            showError(error.response.data);
        });
    }

    handleLeague(event) {
        this.setState({league: event.target.value},
            function()
            {
                this.update_team_list()
            }
        );
    }

    handleTeamHome(event)
    {
        this.setState({team_home: event.target.value});
    }

    handleTeamGuest(event) {
        this.setState({team_guest: event.target.value});
    }

    handleTeamHomeGoals(event)
    {
        this.setState({team_home_goals: event.target.value});
    }

    handleTeamGuestGoals(event)
    {
        this.setState({team_guest_goals: event.target.value});
    }

    render()
    {
        return (
            <form className='menu_form' id="user-login-form" method="post" onSubmit={(e)=>this._handleSubmit(e)}>
            <fieldset>
                <label htmlFor="id_league">League:</label>
                <select id="id_league" name="league" value={this.state.league}
                    onChange={this.handleLeague} required="true" >
                    { this.state.league_list.map( league =>
                        <option value={league.pk}>{league.name}</option>
                    )}
                </select>

                <label htmlFor="id_team_home">Home team:</label>
                <select id="id_team_home" name="team_home" value={this.state.team_home}
                    onChange={this.handleTeamHome} required="true" >
                    { this.state.team_list.map( team =>
                        <option value={team.pk}>{team.name}</option>
                    )}
                </select>

                <label htmlFor="id_team_home_goals">Home team goals:</label>
                <input
                    id="id_team_home_goals"
                    name="team_home_goals"
                    type="number"
                    min='0'
                    value={this.state.team_home_goals}
                    onChange={this.handleTeamHomeGoals}
                    required="true" />

                <label htmlFor="id_team_guest">Guest team:</label>
                <select id="id_team_guest" name="team_guest" value={this.state.team_guest}
                    onChange={this.handleTeamGuest} required="true" >
                    { this.state.team_list.map( team =>
                        <option value={team.pk}>{team.name}</option>
                    )}
                </select>

                <label htmlFor="id_team_guest_goals">Guest team goals</label>
                <input
                    id="id_team_guest_goals"
                    name="team_guest_goals"
                    type="number"
                    min='0'
                    value={this.state.team_guest_goals}
                    onChange={this.handleTeamGuestGoals}
                    required="true" />

                <button type="submit" className="addmenu_btn" onSubmit={(e)=>this._handleSubmit(e)}>Create match</button>
            </fieldset>
            </form>
        );
    }
}

export default CreateMatchForm
