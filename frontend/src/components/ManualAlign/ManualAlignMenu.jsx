import React, { Component } from 'react';
import { ServerInterface } from '../../ServerInterface';
import Alignment from './children/Alignment';
import { Button } from '@mui/material';

class ManualAlignMenu extends Component {
  constructor(props) {
    super(props);

    this.state = { images: [], };
  }
  getManual = async() => { 
    let image_bytes = await ServerInterface.getAlignmentGrid(3, 3) ;
    let urls = []
    image_bytes.result.forEach(bytes => { urls.push(bytes) });
    this.setState({images: urls});
  }

  render() {
    return (
      <div>
        <Button variant='outlined' onClick={this.getManual.bind(this)}>
          query manual grid
        </Button>
        <Alignment images={this.state.images} />
      </div>
    );
  }
}

export default ManualAlignMenu;
