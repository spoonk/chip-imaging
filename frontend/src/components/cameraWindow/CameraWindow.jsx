import React, { Component } from 'react';
import styles from './CameraWindow.module.css'
import { socket } from '../../socket';
import CameraFeed from '../cameraFeed/CameraFeed';
import { defaultImg } from '../../config';
import CameraControl from '../CameraControl/CameraControl';
import { ServerInterface } from '../../ServerInterface';
import { showToast } from '../../utils';

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
    socket.on('connect', () => {
      console.info('socket connection established')
    });

    socket.on('disconnect', () => {  
      console.info('socket disconnected')
    });

    socket.on('frame', (data) => {
      console.info('got frame')
      var arrayBuffer = new Uint8Array(data['image_data'])
      var blob = new Blob( [arrayBuffer], { type:"image/jpeg" } );
      var img_url = URL.createObjectURL(blob);
      this.setState({ imgUrl: img_url })
    })

    socket.on('message', (data) => {
      console.info(data)
    })
  }

  componentWillUnmount = () => {
    // TODO: this is really bad, later unregister specific listeners
    socket.removeAllListeners()
    socket.disconnect()
  }

  /**
     * Tells the server to start streaming video to this socket
     */
  startVideoFeed = () => {
    console.info('starting the camera feed')
    try { 
      socket.connect();
      socket.emit('video');

    } catch (err) { console.error(err) }
  }

  setGainAndExposure = async(gain, exposure) => {
    showToast(await ServerInterface.setGainExposure(gain, exposure) )
  }

  render() { 
    return ( 
      <div className={styles.camera_window}>
        <div className={styles.camera_stream_container}>
          <CameraFeed imgUrl={this.state.imgUrl} />
          <CameraControl startFeedFN={this.startVideoFeed} setGainExposureFN={this.setGainAndExposure} />
        </div>
      </div>
    );
  }
}

export default CameraWindow;
