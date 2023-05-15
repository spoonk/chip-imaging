import React, { Component } from 'react'
import { useEffect, useState } from 'react'
import ImageCanvas from './ImageCanvas'
import Draggable from 'react-draggable'
import { Button, ButtonGroup, TextField } from '@mui/material' 

const Alignment = ({images}) => {
  // have a controls component and a visualizer component
  // (wow such an original idea)
  const [theta, setTheta] = useState(0.05)
  const [pixPerUM, setPixPerUM] = useState(0.6265)
  const [distanceUM, setDistanceUM] = useState(1500.0)

  // image canvas is the visualizer
  // some other controls component later (or no component and just in this one)
  // this component should also handle grabbing the images later too
  return (
    <>
      {/*TODO: display theta*/}
      <div className="alignment-controls">

        <ButtonGroup orientation="vertical" variant="outlined" >
          {/* TODO: theta number input, distance number input, pixperum input  */}
          <Button onClick={() => setTheta(theta + 0.01)}>
             increment theta by 0.01
          </Button>

          <Button onClick={() => setTheta(theta - 0.01)}>
             decrement theta by 0.01
          </Button>

        </ButtonGroup>
      </div>
      <div className='alignment-container'>
          <ImageCanvas 
            images={images}
            rows={3}
            cols={3}
            pixelsPerUM={pixPerUM}
            theta={theta}
            distance={distanceUM}
          />
      </div>

    </>
  )
} // Alignment

export default Alignment
