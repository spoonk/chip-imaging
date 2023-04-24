import React, { Component } from 'react';
import CameraWindow from '../cameraWindow/CameraWindow';
import styles from "./AppContainer.module.css"
import Control from '../Control/Control';

class AppContainer extends Component {
    render() { 
        return ( 
            <div className={styles.app_container}>
                <CameraWindow />
                <Control />
            </div>
        );
    }
}
 
export default AppContainer;