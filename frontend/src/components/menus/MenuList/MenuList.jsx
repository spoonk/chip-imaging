import React, { Component } from 'react';
import styles from "./MenuList.module.css"

class MenuList extends Component {
    constructor(props) {
        super(props);
    }
    render() { 
        return (  
            <div className={styles.menu_list}>
                {
                    this.props.menus.map(menu => {
                        return (<h2>{menu[0]}</h2>)
                    })
                }
            </div>
        );
    }
}
 
export default MenuList;