import {sendDelete} from '../ajax.jsx';
import axios from 'axios';
import TeamStatList from './teamstatlist.component.jsx';
import Return from './return.component.jsx';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';
import CreateLeagueForm from '../create/createleague.component.jsx';

class LeaguesList extends Component
{
    constructor(props) {
    super(props);
    this.url = '/fifa/api/leagues/';
    this.handleClick = this.handleClick.bind(this);
    this.handleEdit = this.handleEdit.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
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

    handleEdit(e)
    {
        var league_pk = e.target.getAttribute('data-pk');
        axios.get('/fifa/api/leagues/' + league_pk + "/get_info/")
            .then(res => {
                var league = res.data;
                ReactDOM.render(
                    <CreateLeagueForm league={league} />,
                    document.getElementById('edit-container')
                );
                document.getElementById('fullscreen-edit-div').classList.remove('animation_to');
                document.getElementById('fullscreen-edit-div').classList.add('animation_from');
        });
    }

    handleDelete(e)
    {
        var league_pk = e.target.getAttribute('data-pk');
        sendDelete.delete('/fifa/api/leagues/' + league_pk + '/delete/')
            .then(res =>{
                showSuccess('Successfuly delete league!');
                axios.get(this.url)
                    .then(res => {
                        const leagues = res.data;
                        this.setState({ leagues });
                    });

            }).catch(function (error) {
                showError(error.response.data.message);
            });
    }

    render()
    {
        return (
            <div>
            { this.state.leagues.map(league =>
            <div className="league_block">
                <div className="league_div">
                <img className="league_img" alt={league.shortcut} src={league.logo} />
                <h3 data-shortcut={league.shortcut} data-pk={league.pk} onClick={(e)=>this.handleClick(e)}>{league.name}</h3>
                <h2>Author: {league.author.username}</h2>
                <p>{league.short_description}</p>
                { league.author.username == username &&
                    <button onClick={this.handleEdit} data-pk={league.pk}>Edit</button>
                }
                { league.author.username == username &&
                    <button onClick={this.handleDelete} data-pk={league.pk}>Delete</button>
                }
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
