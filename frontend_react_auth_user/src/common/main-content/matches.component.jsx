import axios from 'axios';
import React, { Component } from 'react';

class Matches extends Component
{
    constructor(props)
    {
        super(props);
        this.statpk = this.props.stat;
        this.state = {
            matches: []
        };
    }

    componentDidMount() {
        axios.get('/fifa/api/teamstats/' + this.statpk + '/get_matches/')
            .then(res => {
                const matches = res.data;
                this.setState({ matches });
        });
    }

    render()
    {
        return (
            <div className='matches_container'>
                <h1 className='title'>Matches</h1>
                { this.state.matches.map(match =>
                <div className='match_block'>
                    <h1 className='match_score'>
                        {match.team_home_goals} - {match.team_guest_goals}
                    </h1>
                    <h1>Home - Guest</h1>
                    <h1 className='match_teams'><strong>{match.teamstat_team_home.name}</strong>
                        - {match.teamstat_team_guest.name}</h1>
                <br />
                <hr className="separate_line" />
                </div>
                )}
            </div>
        )
    }
}

export default Matches
