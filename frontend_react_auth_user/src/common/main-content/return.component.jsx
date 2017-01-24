import TeamStatList from './teamstatlist.component.jsx';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import LeaguesList from './leagues.component.jsx';

class Return extends Component
{
    constructor(props)
    {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(event)
    {
        if(this.props.path === '')
        {
            ReactDOM.render(
                <LeaguesList />,
                document.getElementById('main')
            );
            document.getElementById('return-div').innerHTML = '';
        }
        else
        {
            ReactDOM.render(
                <TeamStatList statpk={this.props.path} />,
                document.getElementById('main')
            );
            ReactDOM.render(
                <Return path='' />,
                document.getElementById('return-div')
            );
        };
    }

    render()
    {
        return (
            <img className='return_arrow' onClick={this.handleClick} src='/static/fifa_league/gfx/return-arrow.svg'/>
        )
    }
}

export default Return
