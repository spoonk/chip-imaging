import React, { Component } from 'react';
import styles from "./InputField.module.css"

class InputField extends Component {
    constructor(props) {
        super(props);
        this.state = {
            value: "",
            focused: false,
            labelClass: styles.label_empty
        }
    }
    
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

        // TODO: have a callback as a prop
        this.setState({value: e.target.value})
    }

    handleFocus = () => {
        this.setState({labelClass: styles.label_nonempty})
    }

    handleBlur = () => {
        // console.log('blur')
        if (this.state.value !== "") return;
        this.setState({labelClass: styles.label_empty})
    }

    render() { 
        return (  
            <div className={styles.input_field}>
                <div className={styles.label + " " + this.state.labelClass}>
                    {this.props.name}
                </div>
                <input
                    onChange={this.handleChange.bind(this)}
                    className={styles.input_bar}
                    value={this.state.value} 
                    onFocus={this.handleFocus.bind(this)}
                    onBlur={this.handleBlur.bind(this)}
                    >
                </input>
            </div>
        );
    }
}
 
export default InputField;