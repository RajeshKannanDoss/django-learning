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

    componentDidMount()
    {
        document.getElementById('current-email').innerHTML = 'Current email: ' + user_email;
    }

    _handleSubmit(e)
    {
        e.preventDefault();
        var user_new_email = this.state.new_email;
        sendURLEncodedForm.post(this.url, qs.stringify({
            new_email: user_new_email
        }))
        .then(function (response) {
            showSuccess(response.data);
            user_email = user_new_email;
            document.getElementById('current-email').innerHTML = 'Current email: ' + user_email;
            document.getElementById('id_new_email').value = '';
        })
        .catch(function (error) {
            showError(error);
        });
    }

    handleNewEmail(event) {
        this.setState({new_email: event.target.value});
    }

    render()
    {
        return (
        <div>
            <h1 className='current_email' id='current-email'></h1>
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
