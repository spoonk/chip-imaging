import React, { Component } from 'react';
import styles from "./ConfigMenu.module.css"
import Button from '../../Button/Button';
import InputField from '../../InputField/InputField';

class ConfigMenu extends Component {
    constructor(props) {
        super(props);
        this.state = {
            width : 1000,
            height : 1000,
            distance:500,
        }
    }

    saveConfig = async() => { }
    saveCorner = async() => { }

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
                            <Button 
                                name="save position as top-left corner"
                                callback={this.saveCorner.bind(this)}
                            />
                            <InputField 
                                name="distance between snapshots (um)"
                                changeCB={(val) => {this.setState({distance: val})}}
                                value={this.state.distance}
                            />
                        </div>

                        <div className={styles.input_column}>
                            <InputField 
                                name="width of stitched image (um)"
                                changeCB={(val) => {this.setState({width: val})}}
                                value={this.state.width}
                            />
                            <InputField 
                                name="height of stitched image (um)"
                                changeCB={(val) => {this.setState({height: val})}}
                                value={this.state.height}
                            />
                        </div>
                        
                    </div>

                    <Button 
                        name="save configuration"
                        callback={this.saveConfig.bind(this)}
                    />
                </div>

            </div>
        );
    }
}
 
export default ConfigMenu;