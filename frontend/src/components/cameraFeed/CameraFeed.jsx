import React, { Component } from 'react';
import styles from "./CameraFeed.module.css"

class CameraFeed extends Component {
    constructor(props) {
        super(props);
    }

    render() { 
        return (  
      <div className={styles.camera_feed_container}>
        <img 
          className={styles.camera_feed}
          src={this.props.imgUrl} 
          alt="camera feed frame" 
        />
      </div>
    );
  }
} // class CameraFeed

export default CameraFeed;
