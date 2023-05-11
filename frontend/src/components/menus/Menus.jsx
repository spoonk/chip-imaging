import React, { Component } from 'react';
import InitializationMenu from './InitializationMenu/InitializationMenu';
import AcquisitionMenu from './AcquisitionMenu/AcquisitionMenu';
import StitchingMenu from './StitchingMenu/StitchingMenu';
import ConfigMenu from './ConfigMenu/ConfigMenu';
import ManualAlign from '../ManualAlign/ManualAlign';
// const nameToComp = {
//     "initialization": ["initialization", <InitializationMenu />],
//     "configuration": ["configuration", <ConfigMenu />],
//     "acquisition": ["acquisition", <AcquisitionMenu />],
//     "stitching": ["stitching", <StitchingMenu />],
// };


const menuArr = [
    ["initialization", <InitializationMenu />],
    ["configuration", <ConfigMenu />],
    ["acquisition", <AcquisitionMenu />],
    ["stitching", <StitchingMenu />],
    ["manual rotation", <ManualAlign />],
];

export default menuArr;