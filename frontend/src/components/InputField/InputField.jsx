import React, { Component } from 'react';
import styles from "./InputField.module.css"


/**
 * props
 * 
 * name: the label of the input field
 * changeCB: the callback function that is
 *      called when the value in the input changes
 *      (used for updating value)
 * 
 * value: the value displayed in the input field
 */

class InputField extends Component {
    
    isNumber = (str) => {
        // https://stackoverflow.com/a/175787
        if (typeof str != "string") return false // we only process strings!  
        return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
                !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail    
    }

    isValidInput = (str) => {
        return str === "" || this.isNumber(str);
    }

    handleChange = (e) => {
        if (!this.isValidInput(e.target.value)) return;
        console.log('how')
        this.props.changeCB(e.target.value);
    }

    render() { 
        return (  
            <div className={styles.input_field}>
                <div className={styles.label}>
                    {`${this.props.name}:`}
                </div>
                <input
                    onChange={this.handleChange.bind(this)}
                    className={styles.input_bar}
                    value={this.props.value} 
                    >
                </input>
            </div>
        );
    }
}
 
export default InputField;