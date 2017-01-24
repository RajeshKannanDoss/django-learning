import React, { Component } from 'react';
import {instance} from '../ajax.jsx';
var qs = require('qs');
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';

class LoginForm extends Component
{
    constructor(props)
    {
        super(props);
        this.url = '/fifa/login_user/';
        this.state = {username:'', password:''};
        this.handleUsername = this.handleUsername.bind(this);
        this.handlePassword = this.handlePassword.bind(this);
    }

    _handleSubmit(e)
    {
        e.preventDefault();
        instance.post(this.url, qs.stringify({
            username: this.state.username,
            password: this.state.password
        }))
        .then(function (response) {
            showSuccess(response.data);
            location.reload();
        })
        .catch(function (error) {
            showError(error.response.data);
        });
    }

    handleUsername(event) {
        this.setState({username: event.target.value});
    }

    handlePassword(event)
    {
        this.setState({password: event.target.value});
    }

    render()
    {
        return (
            <form className='menu_form' id="user-login-form" method="post" onSubmit={(e)=>this._handleSubmit(e)}>
            <fieldset>

                <label htmlFor="id_username">Username:</label>
                <input
                    id="id_username"
                    name="username"
                    type="text"
                    value={this.state.username}
                    onChange={this.handleUsername}
                    required="true" />

                <label htmlFor="id_password">Password:</label>
                <input
                    id="id_password"
                    name="password"
                    type="password"
                    value={this.state.password}
                    onChange={this.handlePassword}
                    required="true" />

                <button type="submit" className="addmenu_btn" onSubmit={(e)=>this._handleSubmit(e)}>Log in</button>
            </fieldset>
            </form>
        );
    }
}

export default LoginForm
