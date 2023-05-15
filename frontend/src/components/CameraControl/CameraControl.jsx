import React, { Component } from 'react';
import { Button, ButtonGroup, TextField } from '@mui/material'; 
import styles from './CameraControl.module.css'
import InputField from '../InputField/InputField';
class CameraControl extends Component {
  constructor(props) {
    super(props)
    this.state = {
      exposureVal: 100,
      gainVal: 1,
    }
  }

  changeExposureCB = (exposure) => { this.setState({exposureVal: exposure}) }
  changeGainCB = (gain) => { this.setState({gainVal: gain}) }
  setGainExposure = () => { this.props.setGainExposureFN(this.state.gainVal, this.state.exposureVal) }

  render() { 
    return (  
      <div className={styles.camera_control}>
        <div className={styles.input_container}>
          <TextField
            label="exposure(ms)"
            type="number"
            InputLabelProps={{ shrink: true, }}
            value = {this.state.exposureVal}
            onChange ={(e) => { this.changeExposureCB(e.target.value) }}
          />
          <TextField
            label="gain"
            type="number"
            InputLabelProps={{ shrink: true, }}
            value = {this.state.gainVal}
            onChange ={(e) => { this.changeGainCB(e.target.value) }}
          />
        </div>
        <div className={styles.button_container}>
          <ButtonGroup orientation="horizontal" variant="outlined" fullWidth={true}>
            <Button onClick={this.props.startFeedFN}>
              start camera feed
            </Button>
            <Button onClick={this.setGainExposure.bind(this)}>
              set gain and exposure
            </Button>
          </ButtonGroup>
        </div>
      </div> 
    );
  }
}

export default CameraControl;
