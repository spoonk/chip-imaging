import React, { Component } from 'react';
import styles from "./ConfigMenu.module.css"
import { Button, TextField } from '@mui/material';
import { ServerInterface } from '../../../ServerInterface';
import { showToast } from '../../../utils';

class ConfigMenu extends Component {
  constructor(props) {
    super(props);
    this.state = {
      width : 1000,
      height : 1000,
      distance:500,
    }
  }

  saveCorner = async() => { showToast(await ServerInterface.saveTopLeftPosition()) }
  saveConfig = async() => { 
    showToast(await ServerInterface.setImagingParameters(
      this.state.width, this.state.height, this.state.distance))
  }

  render() { 
    return (  
      <div className="menu">
        {
          /**
           * set top left position
           * set width 
           * set height
           * set distance between snapshots
           * update configuration
           */
        }
        <div className={styles.container}>

          <div className={styles.column_wrapper}>

            <div className={styles.input_column}>

              <Button variant="outlined" onClick={this.saveCorner.bind(this)}>
                save position as top left corner of chip
              </Button>

              <TextField
                label="distance between images (um)"
                type="number"
                InputLabelProps={{ shrink: true, }}
                value = {this.state.distance}
                onChange ={(e) => {this.setState({distance: e.target.value})}}
              />

            </div>

            <div className={styles.input_column}>

              <TextField
                label="width of stitched image (um)"
                type="number"
                InputLabelProps={{ shrink: true, }}
                value = {this.state.width}
                onChange ={(e) => {this.setState({width: e.target.value})}}
              />

              <TextField
                label="height of stitched image (um)"
                type="number"
                InputLabelProps={{ shrink: true, }}
                value = {this.state.height}
                onChange ={(e) => {this.setState({height: e.target.value})}}
              />

            </div>

          </div>

          <Button variant='contained' onClick={this.saveConfig.bind(this)}
          >Save configuration</Button>

        </div>

      </div>
    );
  }
}

export default ConfigMenu;
