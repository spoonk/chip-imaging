import React, { Component } from 'react';
import Button from '../../Button/Button';
import { ServerInterface } from '../../../ServerInterface';

class InitializationMenu extends Component {
    constructor(props) {
        super(props);
    }

    getName = () => { return "Initialization" }

    initializeDevice = () => { ServerInterface.initialize() }
    getStatus = () => { ServerInterface.getStatus() }

    render() { 
        return (  
            <div className="menu">
                { /** * connect to device */ }
                <Button 
                    name="initialize the device"
                    callback={this.initializeDevice.bind(this)}
                />
                <Button 
                    name="get status"
                    callback={this.getStatus.bind(this)}
                />
            </div>
        );
    }
}
 
export default InitializationMenu;