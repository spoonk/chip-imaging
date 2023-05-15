import React, { Component } from 'react';
import CameraWindow from '../cameraWindow/CameraWindow';
import styles from "./AppContainer.module.css"
import Control from '../Control/Control';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.min.css'

class AppContainer extends Component {
  constructor(props) {
    super(props)
    this.state = { deviceStatus: {} }
  }

  getDeviceStatus = async() => {
    // fetches status from the server
    // this is an object that will contain
    // - which operation is currently running
    // - imaging grid configuration
    // - if device is initialized
    try {

    } catch {

    }
  }

  componentDidMount = () => { this.getDeviceStatus() }

  render() { 
    return ( 
      <div className={styles.app_container}>
        <CameraWindow status={this.state.deviceStatus} />
        <Control status={this.state.deviceStatus} />
        <ToastContainer />

      </div>
    );
  }
}

export default AppContainer;
