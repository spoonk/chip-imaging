import React, { Component } from 'react';
import Button from '../Button/Button';
import styles from './CameraControl.module.css'
import InputField from '../InputField/InputField';

class CameraControl extends Component {
    render() { 
        return (  
           <div className={styles.camera_control}>
                {
                    /**
                     * two input fields (exposure, gain)
                     * a button to start the feed
                     * a button to update the parameters
                     */
                }
                <div className={styles.input_container}>
                    <InputField 
                        name='exposure'
                    />
                    <InputField 
                        name='gain'
                    />
                </div>
                <div className={styles.button_container}>
                    <Button 
                        callback={this.props.startFeedFN} 
                        name={'start camera feed'}
                    />
                    <Button 
                        callback={this.props.startFeedFN} 
                        name={'set gain and exposure'}
                    />
                </div>
           </div> 
        );
    }
}
 
export default CameraControl;