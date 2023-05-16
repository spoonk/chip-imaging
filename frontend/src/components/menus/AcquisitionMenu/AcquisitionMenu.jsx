import React, { Component } from 'react';
/* import Button from '../../Button/Button'; */
import { ButtonGroup, Button } from '@mui/material';
import { ServerInterface } from '../../../ServerInterface';
import { showToast } from '../../../utils';

class AcquisitionMenu extends Component {
  beginAcquisition = async() => {
    showToast(await ServerInterface.acquire())
  }
  promptDirectory  = async() => { 
    showToast(await ServerInterface.promptPath()) 
  }

  render() { 
    return (  
      <div className="menu">

        <ButtonGroup orientation="vertical" variant="outlined" >
          <Button onClick={this.beginAcquisition.bind(this)}>
            begin acquisition
          </Button>

          <Button onClick={this.promptDirectory.bind(this)}>
            select data path
          </Button>

        </ButtonGroup>

      </div>
    );
  }
}

export default AcquisitionMenu;
