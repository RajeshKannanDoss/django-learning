import Return from './return.component.jsx';
import TeamMain from './teammain.component.jsx';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

class TeamStatList extends Component
{
    constructor(props) {
    super(props);
    this.statpk = this.props.statpk;
    this.handleClick = this.handleClick.bind(this);
    this.state = {
        teamstats: []
    };
    }

    componentDidMount() {
        axios.get('/fifa/api/leagues/' + this.statpk + '/get_teamstat_list/')
            .then(res => {
                const teamstats = res.data;
                this.setState({ teamstats });
            });
    }

    handleClick(e)
    {
        ReactDOM.render(
            <Return path={e.target.getAttribute('data-leaguepk')} />,
            document.getElementById('return-div')
        );

        ReactDOM.render(
            <TeamMain stat={e.target.getAttribute('data-statpk')} />,
            document.getElementById('main')
        );
    }

    render()
    {
        return (
        <table className="teams_table">
            <thead>
            <tr>
                <th>Team</th>
                <th>Count</th>
                <th>Wins</th>
                <th>Loses</th>
                <th>Draws</th>
                <th>Goals SC</th>
                <th>Goals CN</th>
                <th>Points</th>
            </tr>
            </thead>
            <tbody>
            { this.state.teamstats.map(teamstat =>
            <tr>
                <td>
                    <img className='team_logo' alt={teamstat.team.shortcut} src={teamstat.team.logo} />
                    <h3 data-leaguepk={teamstat.league} data-statpk={teamstat.pk} onClick={(e)=>this.handleClick(e)}> {teamstat.team.name} </h3>
                </td>
                <td> {teamstat.match_count} </td>
                <td> {teamstat.wins} </td>
                <td> {teamstat.loses} </td>
                <td> {teamstat.draws} </td>
                <td> {teamstat.goals_scored} </td>
                <td> {teamstat.goals_conceded} </td>
                <td> {teamstat.points} </td>
            </tr>
            )}
            </tbody>
        </table>
        )
    }
}

export default TeamStatList
