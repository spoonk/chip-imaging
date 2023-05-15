import React from 'react'
import { useState } from 'react'
import ImageCanvas from './ImageCanvas'
import { Button, ButtonGroup, TextField } from '@mui/material' 
import { ServerInterface } from '../../../ServerInterface'
import { toast } from 'react-toastify'

const Alignment = () => {
  // have a controls component and a visualizer component
  // (wow such an original idea)
  const [theta, setTheta] = useState(0.05)
  const [pixPerUM, setPixPerUM] = useState(0.6265)
  const [distanceUM, setDistanceUM] = useState(1500.0)
  const [images, setImages] = useState([])

  // amount to zoom into the canvas by 
  // larger values correspond to being more zoomed in on the image
  const [zoom, setZoom] = useState(1.0);
  const zoomOut = () => {
    // never scale by a negative amount
    const zoomAmt = Math.max(zoom - 0.1, 0.1);
    setZoom(zoomAmt);
  }

  const getManual = async() => { 
    let image_bytes = await ServerInterface.getAlignmentGrid(3, 3) ;
    let urls = []
    image_bytes.result.forEach(bytes => { urls.push(bytes) });
    toast.success("images loaded", {
      position: "bottom-left",
    })
    setImages(urls)
  }

  // don't need to bound zooming out
  const zoomIn = () => { setZoom(zoom + 0.1) }
  // image canvas is the visualizer
  // some other controls component later (or no component and just in this one)
  // this component should also handle grabbing the images later too
  return (
    <div className='alignment-container'>
      {/*TODO: display theta*/}
      <ImageCanvas 
        images={images}
        rows={3}
        cols={3}
        pixelsPerUM={pixPerUM}
        theta={theta}
        distance={distanceUM}
        zoom={zoom}
      />
      <div className='canvas-controls'>
        <ButtonGroup orientation="vertical" variant="contained" >
          {/* TODO: theta number input, distance number input, pixperum input  */}

          <Button variant='contained' onClick={() => getManual()}>
            query manual grid
          </Button>
          <TextField 
            label="rotation (rad)"
            variant='filled'
            type="number"
            InputLabelProps={{ shrink: true, }}
            value = {theta}
            onChange ={(e) => {setTheta(e.target.value)}}
          />

        </ButtonGroup>

        <ButtonGroup variant='contained' orientation='horizontal'>
          <Button onClick={()=>{zoomIn()}}> + </Button>           
          <Button onClick={()=>{zoomOut()}}> - </Button>           
        </ButtonGroup>

      </div>

    </div>
  )
} // Alignment

export default Alignment
