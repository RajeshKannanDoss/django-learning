import React, { Component } from 'react';
import { sendURLEncodedForm } from '../ajax.jsx';
import axios from 'axios';
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';
var qs = require('qs');

class CreateTeamStatForm extends Component
{
    constructor(props)
    {
        super(props);
        this.url = '/fifa/api/teamstat/';
        this.state = {team:'', league:'',
            team_list: [], league_list: []};
        this.handleTeam = this.handleTeam.bind(this);
        this.handleLeague = this.handleLeague.bind(this);
    }

    componentDidMount() {
        axios.get('/fifa/api/teams/')
            .then(res => {
                const team_list = res.data;
                this.setState({ team_list });
                this.setState({team: team_list[0]['shortcut']});
        });
        axios.get('/fifa/api/leagues/')
            .then(res => {
                const league_list = res.data;
                this.setState({ league_list });
                this.setState({league: league_list[0]['shortcut']})
        });
    }

    _handleSubmit(e)
    {
        e.preventDefault();

        sendURLEncodedForm.post(this.url, qs.stringify({
            team: this.state.team,
            league: this.state.league
        }))
        .then(function (response) {
            showSuccess(response.data);
        })
        .catch(function (error) {
            showError(error.response.data);
        });
    }

    handleLeague(event) {
        this.setState({league: event.target.value});
    }

    handleTeam(event)
    {
        this.setState({team: event.target.value});
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
                        <option value={league.shortcut}>{league.name}</option>
                    )}
                </select>

                <label htmlFor="id_team">Team:</label>
                <select id="id_team" name="team" value={this.state.team}
                    onChange={this.handleTeam} required="true" >
                    { this.state.team_list.map( team =>
                        <option value={team.shortcut}>{team.name}</option>
                    )}
                </select>
                <button type="submit" className="addmenu_btn" onSubmit={(e)=>this._handleSubmit(e)}>Add team to league</button>
            </fieldset>
            </form>
        );
    }
}

export default CreateTeamStatForm
