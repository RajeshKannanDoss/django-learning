import axios from 'axios';
import TeamDescription from './teamdescription.component.jsx';
import Players from './players.component.jsx';
import Matches from './matches.component.jsx';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';

class TeamMain extends Component
{
    constructor(props) {
        super(props);
        this.statpk = this.props.stat;
        this.team = {};
    }

    componentDidMount() {
        axios.get('/fifa/api/teamstats/' + this.statpk + '/get_team/')
            .then(res => {
                this.team = res.data;
                ReactDOM.render(
                    <TeamDescription team={this.team} />,
                    document.getElementById('team-description')
                );
                ReactDOM.render(
                    <Players teampk={this.team.pk} />,
                    document.getElementById('players')
                );
            });
        ReactDOM.render(
            <Matches stat={this.statpk} />,
            document.getElementById('matches')
        );
    }

    render()
    {
        return (
            <div className='main_container'>
                <div id='team-description'></div>
                <div id='matches'></div>
                <div id='players'></div>
            </div>
        )
    }
}

export default TeamMain
