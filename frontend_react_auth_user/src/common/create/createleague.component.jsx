import React, { Component } from 'react';
import { sendFormData } from '../ajax.jsx';
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';
import LeaguesList from '../main-content/leagues.component.jsx';

class CreateLeagueForm extends Component
{
    constructor(props)
    {
        super(props);
        if(this.props.league != '')
        {
            this.state = {
                name: this.props.league.name,
                shortcut: this.props.league.shortcut,
                short_description: this.props.league.short_description,
                full_description: this.props.league.full_description,
                logo: this.props.league.logo,
                imagePreviewUrl: this.props.league.logo
            };
            this.logo = this.props.league.logo;
            this.url = '/fifa/api/leagues/' + this.props.league.pk + '/';
            this.is_update = true;
        } else {
            this.url = '/fifa/api/leagues/';
            this.state = {name:'', shortcut:'', short_description:'',
            full_description:'', logo: ''};
            this.logo = '';
            this.is_update = false;
        }
        this.handleName = this.handleName.bind(this);
        this.handleShortcut = this.handleShortcut.bind(this);
        this.handleShortDescription = this.handleShortDescription.bind(this);
        this.handleFullDescription = this.handleFullDescription.bind(this);
        this.handleLogo = this.handleLogo.bind(this);
    }

    componentWillReceiveProps(nextProps)
    {
        this.setState({
            name: nextProps.league.name,
            shortcut: nextProps.league.shortcut,
            short_description: nextProps.league.short_description,
            full_description: nextProps.league.full_description,
            logo: nextProps.league.logo,
            imagePreviewUrl: nextProps.league.logo
        });
    }

    _handleSubmit(e)
    {
        e.preventDefault();
        var data = new FormData();
        data.append('name', this.state.name);
        data.append('shortcut', this.state.shortcut);
        data.append('short_description', this.state.short_description);
        data.append('full_description', this.state.full_description);
        data.append('logo', this.logo);
        if(this.is_update === false){
        sendFormData.post(this.url, data)
        .then(function (response) {
            showSuccess(response.data);
        })
        .catch(function (error) {
            showError(error.response.data);
        });
        } else {
            sendFormData.put(this.url, data)
            .then(function (response) {
                showSuccess(response.data);
                ReactDOM.render(
                    <LeaguesList />,
                    document.getElementById('main')
                );
            })
            .catch(function (error) {
                showError(error.response.data);
            });
        }
    }

    handleName(event) {
        this.setState({name: event.target.value});
    }

    handleShortcut(event)
    {
        this.setState({shortcut: event.target.value});
    }

    handleShortDescription(event)
    {
        this.setState({short_description: event.target.value});
    }

    handleFullDescription(event)
    {
        this.setState({full_description: event.target.value});
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

                <label htmlFor="id_shortcut">Shortcut:</label>
                <input
                    id="id_shortcut"
                    name="shortcut"
                    type="text"
                    pattern='[A-Za-z0-9]+'
                    value={this.state.shortcut}
                    onChange={this.handleShortcut}
                    required="true" />

                <label htmlFor="id_short_description">Short description:</label>
                <input
                    id="id_short_description"
                    name="short_description"
                    type="text"
                    value={this.state.short_description}
                    onChange={this.handleShortDescription}
                    required="true" />
                <label htmlFor="id_full_description">Full description:</label>
                <textarea
                    id="id_full_description"
                    name="full_description"
                    type="textarea"
                    value={this.state.full_description}
                    onChange={this.handleFullDescription}
                    required="true" />
                <label htmlFor="id_logo">Logo (not required)</label>
                    <input
                        id="id_logo"
                        name="logo"
                        type="file"
                        onChange={this.handleLogo} />

                <div className='image_preview_div'>
                    {$imagePreview}
                </div>
                <button type="submit" className="addmenu_btn" onSubmit={(e)=>this._handleSubmit(e)}>Create league</button>
            </fieldset>
            </form>
        );
    }
}

export default CreateLeagueForm
