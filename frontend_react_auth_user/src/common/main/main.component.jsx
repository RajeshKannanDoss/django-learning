import React, {Component} from 'react';
import Profile from './profile.component.jsx';
import ReactDOM from 'react-dom';
import { Link } from 'react-router';
import CreateLeagueForm from '../create/createleague.component.jsx'

class Main extends Component
{
    constructor(props)
    {
        super(props);
        this.handleCreateItems = this.handleCreateItems.bind(this);
    }

    componentDidMount() {
        ReactDOM.render(
            <Profile />,
            document.getElementById('profile')
        );
    }

    handleCreateItems()
    {
        document.getElementById('fullscreen-forms-div').classList.remove('animation_to');
        document.getElementById('fullscreen-forms-div').classList.add('animation_from');
        ReactDOM.render(
            <CreateLeagueForm league='' />,
            document.getElementById('focus-form')
        );
    }

    render()
    {
        return(
        <div className='main_container'>
            <div className='main_top'>
                <div id='profile'></div>
                <div className='menu_container'>
                    <nav>
                        <ul>
                            <li><Link to='/fifa' activeClassName='active'>Main</Link></li>
                            <li><a onClick={this.handleCreateItems}>Add new items</a></li>
                            <li><Link to='/fifa/settings' activeClassName='active'>Settings</Link></li>
                        </ul>
                    </nav>
                </div>
                <div className='logout_div'>
                    <a className='button-primary' href='/fifa/logout_user/'>Log out</a>
                </div>
            </div>
            <div className='main_content'>
                {this.props.children}
            </div>
        </div>
        );
    }
}

export default Main
