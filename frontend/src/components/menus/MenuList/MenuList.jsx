import React, { Component } from 'react';
import styles from "./MenuList.module.css"

class MenuList extends Component {
    render() { 
        return (  
            <div className={styles.menu_list}>
                {
                    this.props.menus.map(menu => {
                        return (
                            <div className={
                                styles.menu_list_item + " " + (this.props.currentMenu[0] === menu[0] ? styles.item_active : styles.item_inactive)}
                                onClick={() => {this.props.changeMenuCB(menu)}}    
                            >
                                    {menu[0]}
                            </div>
                        );
                    })
                }
            </div>
        );
    }
}
 
export default MenuList;