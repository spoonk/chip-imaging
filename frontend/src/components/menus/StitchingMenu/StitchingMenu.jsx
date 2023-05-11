import React, { Component } from 'react';
import Button from '../../Button/Button';
import { ServerInterface } from '../../../ServerInterface';

class StitchingMenu extends Component {
    constructor(props) {
        super(props);

        this.state = {
            stitchng: false,
            hasResult: false,
            images: [],
            image: null
        }
    }

    startStitching = async() => { }
    getStitched = async() => { }
    getManual = async() => { 
            let image_bytes = await ServerInterface.getAlignmentGrid(3, 3) ;
            let urls = []
            image_bytes.result.forEach(bytes => {
                // console.log("DFKDFSJKFdj")
                // var arrayBuffer = new Uint8Array(bytes)
                // var blob = new Blob( [arrayBuffer], { type:"image/jpeg" } );
                // var img_url = URL.createObjectURL(blob);
                // urls.push(img_url)
                urls.push(bytes)
            })
            this.setState({images: urls})
            console.log(urls)
            this.setState({image: urls[0]});


    }

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
            </div>
        );
    }
}
 
export default StitchingMenu;