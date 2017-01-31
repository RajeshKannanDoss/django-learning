import React, { Component } from 'react';
import { sendFormData } from '../ajax.jsx';
var qs = require('qs');
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';
import ReactDOM from 'react-dom';

class CreateTeamForm extends Component
{
    constructor(props)
    {
        super(props);
        this.url = '/fifa/api/teams/';
        this.state = {name:'', description:'', logo: '', imagePreviewUrl:''};
        this.logo = '';
        this.handleName = this.handleName.bind(this);
        this.handleDescription = this.handleDescription.bind(this);
        this.handleLogo = this.handleLogo.bind(this);
    }

    _handleSubmit(e)
    {
        e.preventDefault();
        var data = new FormData();
        data.append('name', this.state.name);
        data.append('description', this.state.description);
        data.append('logo', this.logo);
        var form = this;
        sendFormData.post(this.url, data)
        .then(function (response) {
            showSuccess(response.data);
            document.getElementById('id_team_logo').value = '';
            form.setState({
                name: '',
                description: '',
                logo: '',
                imagePreviewUrl: ''
            });
        })
        .catch(function (error) {
            showError(error.response.data);
        });
    }

    handleName(event) {
        this.setState({name: event.target.value});
    }

    handleDescription(event)
    {
        this.setState({description: event.target.value});
    }

    handleLogo(event)
    {
        event.preventDefault();
        let reader = new FileReader();
        let file = event.target.files[0];

        reader.onloadend = () => {
            this.setState({
                logo: file,
                imagePreviewUrl: reader.result
            }, function() {
                this.logo = this.state.logo;
            });
        }
        reader.readAsDataURL(file);
    }

    render()
    {
        let {imagePreviewUrl} = this.state;
        let $imagePreview = null;
        if(imagePreviewUrl)
        {
            $imagePreview = (<img className='avatar_preview' src={imagePreviewUrl} />);
        } else {
            $imagePreview = (<div className='previewText'>Please select avatar for preview</div>);
        }
        return (
            <form className='menu_form' id="user-login-form" method="post" onSubmit={(e)=>this._handleSubmit(e)}>
            <fieldset>
                <label htmlFor="id_name">Name:</label>
                <input
                    id="id_name"
                    name="name"
                    type="text"
                    value={this.state.name}
                    onChange={this.handleName}
                    required="true" />

                <label htmlFor="id_short_description">Description:</label>
                <input
                    id="id_short_description"
                    name="short_description"
                    type="text"
                    value={this.state.description}
                    onChange={this.handleDescription}
                    required="true" />
                <label htmlFor="id_logo">Logo (not required):</label>
                    <input
                        id="id_team_logo"
                        name="logo"
                        type="file"
                        onChange={this.handleLogo} />

                <div className='image_preview_div'>
                    {$imagePreview}
                </div>
                <button type="submit" className="addmenu_btn" onSubmit={(e)=>this._handleSubmit(e)}>Create team</button>
            </fieldset>
            </form>
        );
    }
}

export default CreateTeamForm
