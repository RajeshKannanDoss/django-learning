import React, { Component } from 'react';
import { sendFormData } from '../ajax.jsx';
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';
import axios from 'axios';
import ReactDOM from 'react-dom';

class CreatePlayerForm extends Component
{
    constructor(props)
    {
        super(props);
        this.url = '/fifa/api/players/';
        this.state = {name:'', team:'', age:'', photo: '',
        team_list:[]};
        this.photo = '';
        this.handleName = this.handleName.bind(this);
        this.handleTeam = this.handleTeam.bind(this);
        this.handleAge = this.handleAge.bind(this);
        this.handlePhoto = this.handlePhoto.bind(this);
    }

    get_all_teams()
    {
        axios.get('/fifa/api/teams/')
            .then(res => {
                const team_list = res.data;
                this.setState({ team_list });
                this.setState({ team:team_list[0]['pk'] });
        });
    }

    componentDidMount() {
        this.get_all_teams();
    }


    _handleSubmit(e)
    {
        e.preventDefault();
        var data = new FormData();
        data.append('name', this.state.name);
        data.append('team', this.state.team);
        data.append('age', this.state.age);
        data.append('photo', this.photo);
        var form = this;
        sendFormData.post(this.url, data)
        .then(function (response) {
            showSuccess(response.data);
            document.getElementById('id_player_photo').value = '';
            form.get_all_teams();
            form.setState({
                name: '',
                age: '',
                photo: '',
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

    handleTeam(event)
    {
        this.setState({team: event.target.value});
    }

    handleAge(event)
    {
        this.setState({age: event.target.value});
    }

    handlePhoto(event)
    {
        event.preventDefault();
        let reader = new FileReader();
        let file = event.target.files[0];

        reader.onloadend = () => {
            this.setState({
                photo: file,
                imagePreviewUrl: reader.result
            }, function() {
                this.photo = this.state.photo;
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

                <label htmlFor="id_team">Team:</label>
                <select id="id_team" name="team" value={this.state.team}
                    onChange={this.handleTeam} required="true">
                    { this.state.team_list.map( team =>
                        <option value={team.pk}>{team.name}</option>
                    )}
                </select>

                <label htmlFor="id_age">Age:</label>
                <input
                    id="id_age"
                    name="age"
                    type="number"
                    min='0'
                    value={this.state.age}
                    onChange={this.handleAge}
                    required="true" />
                <label htmlFor="id_photo">Photo (not required):</label>
                    <input
                        id="id_player_photo"
                        name="photo"
                        type="file"
                        onChange={this.handlePhoto} />

                <div className='image_preview_div'>
                    {$imagePreview}
                </div>
                <button type="submit" className="addmenu_btn" onSubmit={(e)=>this._handleSubmit(e)}>Create player</button>
            </fieldset>
            </form>
        );
    }
}

export default CreatePlayerForm
