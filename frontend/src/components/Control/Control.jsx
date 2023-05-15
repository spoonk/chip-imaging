import React, { Component } from 'react';
import styles from "./Control.module.css"
import menuArr from '../menus/Menus';

import MenuList from '../menus/MenuList/MenuList';
// NOTE: all menus should handle routing internally to avoid one 
// very large container

// the menus do not need to communicate across each other

class Control extends Component {
  constructor(props) {
    super(props);
    this.state = {currentMenu: menuArr[0]}
  }

  setMenuCB = (menu) => { this.setState({currentMenu: menu}) }

  render() { 
    return (  
      <div className={styles.control_container}>
        {/** Menu list of components to choose */}
        <MenuList 
          menus = {menuArr} 
          changeMenuCB = {this.setMenuCB.bind(this)}
          currentMenu = {this.state.currentMenu}
        />
        {this.state.currentMenu[1]}
      </div>
    );
  }
}

export default Control;
