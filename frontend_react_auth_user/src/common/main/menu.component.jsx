import React, {Component} from 'react';
import { Link } from 'react-router';

class Menu extends Component
{
    render()
    {
        return (
            <nav>
                <ul>
                    <li><Link to='/'>Main</Link></li>
                    <li><Link to='/settings'>Settings</Link></li>
                    <li><Link to='/content'>Content</Link></li>
                </ul>
            </nav>
        );
    }
}

export default Menu
