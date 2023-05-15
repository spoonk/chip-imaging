import React, { Component } from 'react';
/* import Button from '../../Button/Button'; */
import { ButtonGroup, Button } from '@mui/material';  
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
              <ButtonGroup orientation="vertical" variant="outlined" fullWidth={false} size="large">
                <Button onClick={this.initializeDevice.bind(this)}>
                  initialize device
                </Button>
                <Button onClick={this.getStatus.bind(this)}>
                  get status
                </Button> 
              </ButtonGroup>
            </div>
        );
    }
}
 
export default InitializationMenu;
