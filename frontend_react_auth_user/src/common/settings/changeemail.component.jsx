import React, { Component } from 'react';
import {sendURLEncodedForm} from '../ajax.jsx';
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';
var qs = require('qs');

class ChangeEmail extends Component
{
    constructor(props)
    {
        super(props);
        this.userpk = userpk;
        this.user_email = user_email;
        this.url = '/fifa/api/user/' + this.userpk + '/change_email/';
        this.state = {new_email:''};
        this.handleNewEmail = this.handleNewEmail.bind(this);
    }

    _handleSubmit(e)
    {
        e.preventDefault();
        sendURLEncodedForm.post(this.url, qs.stringify({
            new_email: this.state.new_email
        }))
        .then(function (response) {
            showSuccess(response.data);
        })
        .catch(function (error) {
            showError(error.response.data);
        });
    }

    handleNewEmail(event) {
        this.setState({new_email: event.target.value});
    }

    render()
    {
        return (
        <div>
            <h1 className='current_email'>Current email: {this.user_email}</h1>
            <form className='menu_form' id="user-login-form" method="post" onSubmit={(e)=>this._handleSubmit(e)}>
            <fieldset>
                <label htmlFor="id_new_email">Enter new email:</label>
                <input
                    id="id_new_email"
                    name="new_email"
                    type="email"
                    value={this.state.new_email}
                    onChange={this.handleNewEmail}
                    required="true" />
                <button type="submit" className="addmenu_btn" onSubmit={(e)=>this._handleSubmit(e)}>Change email</button>
            </fieldset>
            </form>
        </div>
        );
    }
}

export default ChangeEmail
