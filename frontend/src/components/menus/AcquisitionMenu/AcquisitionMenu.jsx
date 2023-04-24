import React, { Component } from 'react';
import Button from '../../Button/Button';

class AcquisitionMenu extends Component {
    beginAcquisition = async() => { }

    render() { 
        return (  
            <div className="menu">
                <Button 
                    name="begin acquisition"
                    callback={this.beginAcquisition.bind(this)}
                />
            </div>
        );
    }
}
 
export default AcquisitionMenu;