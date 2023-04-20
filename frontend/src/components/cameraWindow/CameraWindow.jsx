import React, { Component } from 'react';
import styles from './CameraWindow.module.css'
import { socket } from '../../socket';
import CameraFeed from '../cameraFeed/CameraFeed';
import { defaultImg } from '../../config';
import CameraControl from '../CameraControl/CameraControl';

/**
 * A CameraWindow is a widget for streaming camera from the microscope
 * It contains a CameraFeed and a CameraController.
 * CameraWindow handles all of the logic of initializing a 
 * websocket with the server and is responsible for managing
 * this connection and rendering new frames in CameraFeed
 */
class CameraWindow extends Component {
    constructor(props) {
        super(props);
        this.state = { imgUrl : defaultImg }
    }

    componentDidMount = () => {
        // TODO: move these into their own functions
        socket.connect();

        socket.on('connect', () => {
            console.info('socket connection established')
        });

        socket.on('disconnect', () => {  
            console.info('socket disconnected')
        });

        socket.on('frame', (data) => {
            var arrayBuffer = new Uint8Array(data['image_data'])
            var blob = new Blob( [arrayBuffer], { type:"image/jpeg" } );
            var img_url = URL.createObjectURL(blob);
            this.setState({ imgUrl: img_url })
        })
    }

    componentWillUnmount = () => {
        // TODO: this is really bad, later unregister specific listeners
        socket.removeAllListeners()
        // if (socket.connected()) 
        socket.disconnect()
    }

    /**
     * Tells the server to start streaming video to this socket
     */
    startVideoFeed = () => {
        console.info('starting the camera feed')
        try { socket.emit('start_feed');
        } catch (err) { console.error(err) }
    }

    render() { 
        return ( 
            <div className={styles.CameraWindow}>
                <CameraFeed imgUrl={this.state.imgUrl} />
                <CameraControl startFeedFN ={this.startVideoFeed} />
            </div>
        );
    }
}
 
export default CameraWindow;