import React, { Component } from 'react';
import LeaguesList from './leagues.component.jsx';
import ReactDOM from 'react-dom';

class MainContent extends Component
{
    componentDidMount() {
        ReactDOM.render(
            <LeaguesList />,
            document.getElementById('main')
        );
    }
    render()
    {
        return (
                <div className='main_container'>
                    <div id='main'></div>
                    <div id='return-div'></div>
                </div>
        );
    }
}

export default MainContent
