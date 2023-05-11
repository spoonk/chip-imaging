import React, { Component } from 'react';
import { ServerInterface } from '../../ServerInterface';
import Button from '../Button/Button';

class ManualAlign extends Component {
    constructor(props) {
        super(props);

        this.state = {
            images: [],
         };
    }
    getManual = async() => { 
            let image_bytes = await ServerInterface.getAlignmentGrid(3, 3) ;
            let urls = []
            image_bytes.result.forEach(bytes => { urls.push(bytes) });
            this.setState({images: urls});
    }

    render() {
        return (
            <div>
                <Button
                    name="query manual grid"
                    callback={this.getManual.bind(this)}
                />
                {
                    this.state.images.map((url, index) => {
                        return(
                            <img 
                                src={"data:image/png;base64, " + url} 
                                alt="camera feed frame" 
                                key={index}
                            />
                        )
                    })
                }
            </div>
        );
    }
}

export default ManualAlign;
