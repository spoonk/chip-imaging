import React, { Component } from 'react';
import { ButtonGroup, Button } from '@mui/material';
import { ServerInterface } from '../../../ServerInterface';
import { showToast } from '../../../utils';
import Alignment from '../../ManualAlign/children/Alignment';

class StitchingMenu extends Component {
  constructor(props) {
    super(props);

    this.state = {
      stitchng: false,
      hasResult: false,
      images: [],
      image: null
    }
  }

  startStitching = async() => {
    showToast(await ServerInterface.startStitching())
  }

  // TODO: this
  getStitched = async() => { }

  render() { 
    return (  
      <div className="menu">

        <Alignment />

        <div className='stitching-controls'>
          <ButtonGroup orientation="vertical" variant="outlined" >

            <Button onClick={this.startStitching.bind(this)}>
              start stitching
            </Button>

            <Button onClick={this.getStitched.bind(this)}>
              preview stitching result
            </Button>

          </ButtonGroup>
        </div>

      </div>
    );
  }
}

export default StitchingMenu;
