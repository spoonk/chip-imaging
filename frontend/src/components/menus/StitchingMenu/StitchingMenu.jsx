import React, { Component } from 'react';
import Button from '../../Button/Button';

class StitchingMenu extends Component {
    constructor(props) {
        super(props);

        this.state = {
            stitchng: false,
            hasResult: false,
        }
    }

    startStitching = async() => { }
    getStitched = async() => { }

    render() { 
        return (  
            <div className="menu">
                <Button
                    name="start stitching"
                    callback={this.startStitching.bind(this)}
                />
                <Button
                    name="get stitching result"
                    callback={this.getStitched.bind(this)}
                />
                {
                    /**
                     * will eventually have an image to display
                     * 
                     * eventually have some way to select a path
                     * and save as tiff file there
                     */
                }
            </div>
        );
    }
}
 
export default StitchingMenu;