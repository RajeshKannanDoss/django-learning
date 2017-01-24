import React, { Component } from 'react';
import ChangePassword from './changepassword.component.jsx';
import ChangeEmail from './changeemail.component.jsx';
import ChangeAvatar from './changeavatar.component.jsx';
import ReactDOM from 'react-dom';

class Settings extends Component
{
    componentDidMount() {
        ReactDOM.render(
            <ChangePassword />,
            document.getElementById('change-password-div')
        );
        ReactDOM.render(
            <ChangeEmail />,
            document.getElementById('change-email-div')
        );
        ReactDOM.render(
            <ChangeAvatar />,
            document.getElementById('change-avatar-div')
        );
    }

    render()
    {
        return(
                <div className='settings_container'>
                    <div id='change-password-div'></div>
                    <div id='change-email-div'></div>
                    <div id='change-avatar-div'></div>
                </div>
        );
    }
}

export default Settings
