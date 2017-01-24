import React, {Component} from 'react';

class Profile extends Component
{
    constructor(props)
    {
        super(props);
        this.state = {
            profile: {
                username: username,
                avatar: avatar
            }
        };

        var avatarurl = this.props.avatarurl;
        if(avatarurl != undefined)
        {
            this.setState({
                profile: {
                    avatar: avatarurl
                }
            });
        }
    }

    componentWillReceiveProps(nextProps)
    {
        var avatarurl = nextProps.avatarurl;
        if(avatarurl != undefined)
        {
            this.setState({
                profile: {
                    avatar: avatarurl,
                    username: username
                }
            });
        }
    }

    render()
    {
        return(
            <div>
                <img className='user_logo' alt={this.state.profile.username} src={this.state.profile.avatar}></img>
                <h4 className='username'>{this.state.profile.username}</h4>
            </div>
        );
    }
}

export default Profile
