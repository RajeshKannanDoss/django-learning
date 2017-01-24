import React, { Component } from 'react';

class GuestProfilePresentation extends Component
{
    constructor(props) {
        super(props);
        this.openGuestForms = this.openGuestForms.bind(this);
    }

    openGuestForms()
    {
        document.getElementById('fullscreen-forms-div').classList.remove('animation_to');
        document.getElementById('fullscreen-forms-div').classList.add('animation_from');
    }

    render() {
        return (
            <div className='btn' onClick={this.openGuestForms}>Log in/Sign up</div>
        );
    }
}

export default GuestProfilePresentation
