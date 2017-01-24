import React, { Component } from 'react';
import sendURLEncodedForm from '../ajax.jsx';
var qs = require('qs');

class ChangePassword extends Component
{
    constructor(props)
    {
        super(props);
        this.userpk = userpk;
        this.url = '/fifa/api/user/' + this.userpk + '/change_password/';
        this.state = {old_password:'', new_password1:'', new_password2:''};
        this.handleOldPassword = this.handleOldPassword.bind(this);
        this.handleNewPassword1 = this.handleNewPassword1.bind(this);
        this.handleNewPassword2 = this.handleNewPassword2.bind(this);
    }

    _handleSubmit(e)
    {
        e.preventDefault();
        sendURLEncodedForm.post(this.url, qs.stringify({
            old_password: this.state.old_password,
            new_password1: this.state.new_password1,
            new_password2: this.state.new_password2,
        }))
        .then(function (response) {
            showSuccess(response.data);
            location.reload();
        })
        .catch(function (error) {
            showError(error.response.data);
        });
    }

    handleOldPassword(event) {
        this.setState({old_password: event.target.value});
    }

    handleNewPassword1(event)
    {
        this.setState({new_password1: event.target.value});
    }

    handleNewPassword2(event)
    {
        this.setState({new_password2: event.target.value});
    }

    render()
    {
        return (
            <form className='menu_form' id="user-login-form" method="post" onSubmit={(e)=>this._handleSubmit(e)}>
            <fieldset>
                <label htmlFor="id_old_password">Old password:</label>
                <input
                    id="id_old_password"
                    name="old_password"
                    type="password"
                    value={this.state.old_password}
                    onChange={this.handleOldPassword}
                    required="true" />

                <label htmlFor="id_new_password1">New password:</label>
                <input
                    id="id_new_password1"
                    name="new_password1"
                    type="password"
                    value={this.state.new_password1}
                    onChange={this.handleNewPassword1}
                    required="true" />

                <label htmlFor="id_new_password2">New password (one more time):</label>
                <input
                    id="id_new_password2"
                    name="new_password2"
                    type="password"
                    value={this.state.new_password2}
                    onChange={this.handleNewPassword2}
                    required="true" />
                <button type="submit" className="addmenu_btn" onSubmit={(e)=>this._handleSubmit(e)}>Change password</button>
            </fieldset>
            </form>
        );
    }
}

export default ChangePassword
