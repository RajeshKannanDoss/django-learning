import React, { Component } from 'react';

class TeamDescription extends Component
{
    constructor(props) {
        super(props);
        this.team = this.props.team;
    }

    render()
    {
        return (
            <div className='description_container'>
                <img alt={this.team.shortcut} src={this.team.logo}/>
                <h1 className='title'>{this.team.name}</h1>
                <p className='description'>{this.team.description}</p>
            </div>
        )
    }
}

export default TeamDescription
