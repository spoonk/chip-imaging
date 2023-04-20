import React, { Component } from 'react';
import Button from '../Button/Button';
import styles from './CameraControl.module.css'

class CameraControl extends Component {
    render() { 
        return (  
           <div className={styles.camera_control}>
             <Button 
                callback={this.props.startFeedFN} 
                name={'start camera feed'}
                />
           </div> 
        );
    }
}
 
export default CameraControl;