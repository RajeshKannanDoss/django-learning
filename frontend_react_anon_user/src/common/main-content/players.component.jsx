import axios from 'axios';
import React, { Component } from 'react';

class Players extends Component
{
    constructor(props)
    {
        super(props);
        this.teampk = this.props.teampk;
        this.state = {
            players: []
        };
    }

    componentDidMount() {
        axios.get('/fifa/api/teams/' + this.teampk + '/get_players/')
            .then(res => {
                const players = res.data;
                this.setState({ players });
        });
    }

    render()
    {
        return (
            <div className='matches_container'>
                <h1 className='title'>Players</h1>
                { this.state.players.map(player =>
                <div className='player_block'>
                    <img src={player.photo} alt={player.name}/>
                    <h1>Name: {player.name}</h1>
                    <h1>Age: {player.age}</h1>
                </div>
                )}
            </div>
        )
    }
}

export default Players
