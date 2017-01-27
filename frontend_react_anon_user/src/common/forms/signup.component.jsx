import React, { Component } from 'react';
import {instance} from '../ajax.jsx';
var qs = require('qs');
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';

class SignUpForm extends Component
{
    constructor(props)
    {
        super(props);
        this.url = '/fifa/create_user/';
        this.state = {username:'', password:'', password1:'', email:''};
        this.handleUsername = this.handleUsername.bind(this);
        this.handlePassword = this.handlePassword.bind(this);
        this.handleEmail = this.handleEmail.bind(this);
        this.handlePassword1 = this.handlePassword1.bind(this);
    }

    _handleSubmit(e)
    {
        e.preventDefault();
        instance.post(this.url, qs.stringify({
            username: this.state.username,
            password: this.state.password,
            password1: this.state.password1,
            email: this.state.email
        }))
        .then(function (response) {
            showSuccess(response.data);
            location.reload();
        })
        .catch(function (error) {
            if(error.response != undefined)
            {
                showError(error.response.data);
            } else
            {
                showError(error)
            }
        });
    }

    handleUsername(event) {
        this.setState({username: event.target.value});
    }

    handlePassword(event)
    {
        this.setState({password: event.target.value});
    }

    handleEmail(event) {
        this.setState({email: event.target.value});
    }

    handlePassword1(event)
    {
        this.setState({password1: event.target.value});
    }

    render()
    {
        return (
            <form className='menu_form' id="user-signup-form" method="post" onSubmit={(e)=>this._handleSubmit(e)}>
            <fieldset>

                <label htmlFor="id_username">Username:</label>
                <input
                    id="id_username"
                    name="username"
                    type="text"
                    value={this.state.username}
                    onChange={this.handleUsername}
                    required="true" />

                <label htmlFor="id_email">Email:</label>
                <input
                    id="id_email"
                    name="email"
                    type="email"
                    value={this.state.email}
                    onChange={this.handleEmail}
                    required="true" />

                <label htmlFor="id_password">Password:</label>
                <input
                    id="id_password"
                    name="password"
                    type="password"
                    value={this.state.password}
                    onChange={this.handlePassword}
                    required="true" />

                <label htmlFor="id_password1">Password (one more time):</label>
                <input
                    id="id_password1"
                    name="password1"
                    type="password"
                    value={this.state.password1}
                    onChange={this.handlePassword1}
                    required="true" />

                <button type="submit" className="addmenu_btn">Create Account</button>
            </fieldset>
            </form>
        );
    }
}

export default SignUpForm
