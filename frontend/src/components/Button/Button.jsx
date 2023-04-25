import React, { Component } from 'react';
import styles from "./Button.module.css"
class Button extends Component {
    render() { 
        return ( 
            <button 
                className={styles.button}
                onClick={() => this.props.callback()}
            >
                {this.props.name}
            </button>
         );
    }
}
 
export default Button;