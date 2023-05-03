import React, { Component } from 'react';
import Button from '../../Button/Button';
import { ServerInterface } from '../../../ServerInterface';

class AcquisitionMenu extends Component {
    beginAcquisition = async() => { ServerInterface.acquire() }
    promptDirectory  = async() => { console.info(await ServerInterface.promptPath()) }

    render() { 
        return (  
            <div className="menu">
                <Button 
                    name="begin acquisition"
                    callback={this.beginAcquisition.bind(this)}
                />
                <Button 
                    name="select data path"
                    callback={this.promptDirectory.bind(this)}
                />
            </div>
        );
    }
}
 
export default AcquisitionMenu;