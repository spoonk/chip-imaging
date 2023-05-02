import React, { Component } from 'react';
import Button from '../Button/Button';
import styles from './CameraControl.module.css'
import InputField from '../InputField/InputField';

class CameraControl extends Component {
    constructor(props) {
        super(props)
        this.state = {
            exposureVal: 100,
            gainVal: 100,
        }
    }

    changeExposureCB = (exposure) => { this.setState({exposureVal: exposure}) }
    changeGainCB = (gain) => { this.setState({gainVal: gain}) }
    setGainExposure = () => { this.props.setGainExposureFN(this.state.gainVal, this.state.exposureVal) }

    render() { 
        return (  
           <div className={styles.camera_control}>
                <div className={styles.input_container}>
                    <InputField 
                        name='exposure(ms)'
                        value = {this.state.exposureVal}
                        changeCB = {this.changeExposureCB.bind(this)}
                    />
                    <InputField 
                        name='gain'
                        value = {this.state.gainVal}
                        changeCB = {this.changeGainCB.bind(this)}
                    />
                </div>
                <div className={styles.button_container}>
                    <Button 
                        callback={this.props.startFeedFN} 
                        name={'start camera feed'}
                    />
                    <Button 
                        callback={this.setGainExposure.bind(this)} 
                        name={'set gain and exposure'}
                    />
                </div>
           </div> 
        );
    }
}
 
export default CameraControl;