import React, { Component } from 'react';
import CameraWindow from '../cameraWindow/CameraWindow';
import styles from "./AppContainer.module.css"
import Control from '../Control/Control';

class AppContainer extends Component {
    constructor(props) {
        super(props)
        this.state = {
            deviceStatus: {}
        }
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

    componentDidMount = () => { this.updateDeviceStatus() }

    render() { 
        return ( 
            <div className={styles.app_container}>
                <CameraWindow status={this.state.deviceStatus} />
                <Control status={this.state.deviceStatus} />
            </div>
        );
    }
}
 
export default AppContainer;