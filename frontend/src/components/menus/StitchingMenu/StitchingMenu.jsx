import React, { Component } from 'react';
import { ButtonGroup, Button } from '@mui/material';
import { ServerInterface } from '../../../ServerInterface';

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

  startStitching = async() => { }
  getStitched = async() => { }

  render() { 
    return (  
      <div className="menu">

        <ButtonGroup orientation="vertical" variant="outlined" >

          <Button onClick={this.startStitching.bind(this)}>
            start stitching
          </Button>

          <Button onClick={this.getStitched.bind(this)}>
            get stitching result
          </Button>

        </ButtonGroup>

      </div>
    );
  }
}

export default StitchingMenu;
