import React, { Component } from 'react';
/* import Button from '../../Button/Button'; */
import { ButtonGroup, Button } from '@mui/material';  
import { ServerInterface } from '../../../ServerInterface';
import { showToast } from '../../../utils';

class InitializationMenu extends Component {
  initializeDevice = async() => { showToast(await ServerInterface.initialize()); }
  getStatus = async () => { 
    let res = await ServerInterface.getStatus()
    res[1] = JSON.stringify(res[1])
    showToast(res)
  }

  render() { 
    return (  
      <div className="menu">
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
