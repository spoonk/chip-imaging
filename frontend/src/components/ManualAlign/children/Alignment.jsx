import React from 'react'
import { useState } from 'react'
import ImageCanvas from './ImageCanvas'
import { Button, ButtonGroup, TextField } from '@mui/material' 
import { ServerInterface } from '../../../ServerInterface'
import { toast } from 'react-toastify'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlassPlus, faMagnifyingGlassMinus } from '@fortawesome/free-solid-svg-icons'
import { showToast } from '../../../utils'


const Alignment = () => {
  // have a controls component and a visualizer component
  // (wow such an original idea)
  const [theta, setTheta] = useState(0.00)
  const [pixPerUM, setPixPerUM] = useState(0.6265)
  const [distanceUM, setDistanceUM] = useState(1500.0)
  const [images, setImages] = useState([])
  const [zoom, setZoom] = useState(0.4);

  const zoomIn = () => { setZoom(zoom + 0.1) }
  const zoomOut = () => {
    const zoomAmt = Math.max(zoom - 0.1, 0.1);
    setZoom(zoomAmt);
  }

  const setParameters = async() => {
    const setRes = await ServerInterface.setStitchingParameters(theta, pixPerUM)
    showToast(setRes)
  }

  const getManual = async() => { 
    let image_bytes = await ServerInterface.getAlignmentGrid(3, 3) ;
    if (!image_bytes[0]){
      showToast(image_bytes)
      return
    }
    console.log(image_bytes)

    let urls = []
    image_bytes = image_bytes[1]
    image_bytes.result.forEach(bytes => { urls.push(bytes) });
    toast.success("images loaded", { position: "bottom-left", })
    setImages(urls)


    // parse out the imaging grid
    const grid = image_bytes.grid
    setDistanceUM(grid.distance)
  }

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
          <TextField 
            label="pixels per um"
            variant='filled'
            type="number"
            InputLabelProps={{ shrink: true, }}
            value = {pixPerUM}
            onChange ={(e) => {setPixPerUM(e.target.value)}}
          />
          <Button variant='contained' onClick={() => {setParameters()}}>
            use these parameters
          </Button>

        </ButtonGroup>


      </div>
      <div className='canvas-zoom'>
        <ButtonGroup variant='contained' orientation='vertical'>
          <Button onClick={()=>{zoomIn()}}>
            <FontAwesomeIcon icon={faMagnifyingGlassPlus}/>
          </Button>           
          <Button onClick={()=>{zoomOut()}}> 
            <FontAwesomeIcon icon={faMagnifyingGlassMinus}/>
          </Button>           
        </ButtonGroup>
      </div>

    </div>
  )
} // Alignment

export default Alignment
