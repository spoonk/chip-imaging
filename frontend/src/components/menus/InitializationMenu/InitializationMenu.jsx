import React, { Component } from 'react';


class InitializationMenu extends Component {
    constructor(props) {
        super(props);
    }

    getName = () => { return "Initialization" }

    render() { 
        console.log('init render')
        return (  
            <h1>init menu</h1>
        );
    }
}
 
export default InitializationMenu;