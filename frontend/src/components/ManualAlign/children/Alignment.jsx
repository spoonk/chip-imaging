import React, { Component } from 'react'
import { useEffect, useState } from 'react'
import ImageCanvas from './ImageCanvas'
import Button from '../../Button/Button'
import Draggable from 'react-draggable'

const Alignment = ({images}) => {
  // have a controls component and a visualizer component
  // (wow such an original idea)
  const [theta, setTheta] = useState(0.05)
  const [pixPerUM, setPixPerUM] = useState(0.6265)
  const [distanceUM, setDistanceUM] = useState(1500.0)

  // useEffect(() => {
  //   setInterval(() => setTheta(theta + 0.01), 500)
  // }, [])
  // image canvas is the visualizer
  // some other controls component later (or no component and just in this one)
  // this component should also handle grabbing the images later too
  return (
    <>
      <div className="alignment-controls">
        <div>
          <Button 
            name={"increment theta by 0.01"} 
            callback={() => {
              setTheta(theta + 0.01)
            }} />
          <Button 
            name={"decrement theta by 0.01"} 
            callback={() => {
              setTheta(theta - 0.01)
            }} />
        </div>
        <div>
          <Button 
            name={"increment theta by 0.001"} 
            callback={() => {
              setTheta(theta + 0.001)
            }} />
          <Button 
            name={"decrement theta by 0.001"} 
            callback={() => {
              setTheta(theta - 0.001)
            }} />
        </div>
        <div>
          <Button 
            name={"increment theta by 0.01"} 
            callback={() => {
              setTheta(theta + 0.01)
            }} />
          <Button 
            name={"decrement theta by 0.01"} 
            callback={() => {
              setTheta(theta - 0.01)
            }} />
        </div>
      </div>
      <div className='alignment-container'>
        <Draggable
          handle=".image-canvas"
        >
          <ImageCanvas 
            images={images}
            rows={3}
            cols={3}
            pixelsPerUM={pixPerUM}
            theta={theta}
            distance={distanceUM}
          />
        </Draggable>
      </div>

    </>
  )
} // Alignment

export default Alignment