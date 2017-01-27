import React, { Component } from 'react';
import { sendFormData } from '../ajax.jsx';
import {showError} from '../notification.jsx';
import {showSuccess} from '../notification.jsx';
import Profile from '../main/profile.component.jsx';
import ReactDOM from 'react-dom';

var qs = require('qs');

class ChangeAvatar extends Component
{
    constructor(props)
    {
        super(props);
        this.state = {file: '', imagePreviewUrl: ''};
        this.avatar = '';
        this.url = '/fifa/api/user/' + userpk + '/change_avatar/';
        this.handleImageChange = this.handleImageChange.bind(this);
    }

    _handleSubmit(e)
    {
        e.preventDefault();
        var data = new FormData();
        data.append('avatar', this.avatar);
        sendFormData.post(this.url, data)
        .then(function (response) {
            response = response.data;
            var url = response.url;
            ReactDOM.render(
                <Profile avatarurl={url} />,
                document.getElementById('profile')
            );
            showSuccess(response.message);
        })
        .catch(function (error) {
            console.log(error);
            showError(error.response.data.message);
        });
    }

    handleImageChange(event) {
        event.preventDefault();
        let reader = new FileReader();
        let file = event.target.files[0];

        reader.onloadend = () => {
            this.setState({
                file: file,
                imagePreviewUrl: reader.result
            }, function() {
                this.avatar = this.state.file;
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
        <div>
            <h1>Change avatar:</h1>
            <form className='menu_form' id="user-login-form" method="post" onSubmit={(e)=>this._handleSubmit(e)}>
            <fieldset>
                <div className='image_preview_div'>
                    {$imagePreview}
                </div>
                <input
                    type="file"
                    onChange={this.handleImageChange}
                    required="true" />
                <button type="submit" className="addmenu_btn" onSubmit={(e)=>this._handleSubmit(e)}>Upload new avatar</button>
            </fieldset>
            </form>
        </div>
        );
    }
}

export default ChangeAvatar
