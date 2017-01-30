import axios from 'axios';
import TeamStatList from './teamstatlist.component.jsx';
import Return from './return.component.jsx';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';

class LeaguesList extends Component
{
    constructor(props) {
    super(props);
    this.url = '/fifa/api/leagues/';
    this.handleClick = this.handleClick.bind(this);
    this.state = {
        leagues: []
    };

    }

    componentDidMount() {
        axios.get(this.url)
            .then(res => {
                const leagues = res.data;
                this.setState({ leagues });
            });
    }

    handleClick(e)
    {
        var statpk = e.target.getAttribute('data-pk');
        ReactDOM.render(
            <TeamStatList statpk={statpk} />,
            document.getElementById('main')
        );
        ReactDOM.render(
            <Return path='' />,
            document.getElementById('return-div')
        );
    }

    render()
    {
        return (
            <div>
            { this.state.leagues.map(league =>
            <div className="league_block">
                <div className="league_div">
                <img className="league_img" alt={league.name} src={league.logo} />
                <h3 data-pk={league.pk} onClick={(e)=>this.handleClick(e)}>{league.name}</h3>
                <h2>Author: {league.author.username}</h2>
                <p>{league.short_description}</p>
                </div>
                <br />
                <hr className="separate_line" />

            </div>
            )}
            </div>
        )
    }

}

export default LeaguesList
