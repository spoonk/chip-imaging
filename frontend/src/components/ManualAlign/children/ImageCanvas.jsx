import React from 'react'
import { useRef, useEffect, useState } from 'react'
import Draggable from 'react-draggable'

/**
 * Takes in a list of images and stitching parameters 
 * and creates a preview of what the stitching would 
 * look like given those parameters
 * 
 * @param images: list of images to render 
 * @param rows: 
 * @param cols: 
 * @param pixelsPerUM: 
 * @param theta: 
 * @param distance: 
 * @param zoom: 
 * @returns 
 */
const ImageCanvas = ({images, rows, cols, pixelsPerUM, theta, distance, zoom, frameRef, gain}) => {
  const canvasRef = useRef(null)
  const [dragOffset, setDragOffset] = useState({x: 0, y: 0})

  // redraw images whenever something changes
  useEffect(() => {
    renderImages();
  }, [images, rows, cols, pixelsPerUM, theta, distance, zoom, frameRef, gain]) // check dependencies later

  const renderImages = () => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    console.log(frameRef.current)


    // scale back to normal so zoom scales linearly
    // also allows us to overwrite entire canvas
    /* ctx.setTransform(1, 0, 0, 1, 0, 0); */
    /* // clear canvas */
    ctx.fillStyle = '#EEEEEE'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    /**/
    /* ctx.scale(zoom, zoom); */

    // generate a list of usable image elements
    const htmlImages = generateHTMLImages(images)
    // paste images into canvas
    const R =   [[Math.cos(theta), -Math.sin(theta)],
      [Math.sin(theta), Math.cos(theta)]]


    // for (let row = htmlImages.length - 1; row >=0; row--){
    //   const image_row = htmlImages[row];
    //   for (let col = image_row.length - 1; col >=0; col--){
    //     const image = image_row[col]
    //     // determine where to place image
    //     // convert to x,y pixel coordinates
    //     const pix_X = distance * col * pixelsPerUM
    //     const pix_Y = distance * row * pixelsPerUM
    //     const rotated = dotProduct(R, [pix_X, pix_Y])
    //     pasteImageIntoCanvas(image,rotated, ctx)
    //   }
    // }
    htmlImages.forEach((image_row, row) => {
      image_row.forEach((image, col) => {
        // determine where to place image
        // convert to x,y pixel coordinates
        const pix_X = distance * col * pixelsPerUM
        const pix_Y = distance * row * pixelsPerUM
        const rotated = dotProduct(R, [pix_X, pix_Y])
        pasteImageIntoCanvas(image,rotated, ctx)
      })
    })
  }

  /**
   * returns a list of HTMLElement images
   * @param images a list of base64 encoded images 
   */
  const generateHTMLImages = (images) => {
    return(
      images.map((image_row) => {
        return image_row.map((image) => {
          const im = document.createElement('img');
          im.src = `data:image/png;base64, ${image}`
          im.alt= "microscope image"
          return im;
        })
      }));
  }

  const pasteImageIntoCanvas = (image, pix_xy, ctx) => {
    ctx.drawImage(image, pix_xy[0], pix_xy[1]);
  }

  /**
     * computes the dot product Mv
     * @param M 2 x 2 matrix
     * @param v 1 x 2 vector
     * (I know dims don't match, just accept it)
   */
  const dotProduct = (M, v) => {
    return [
      v[0] * M[0][0] + v[1] * M[0][1],
      v[0] * M[1][0] + v[1] * M[1][1],
    ];
  }

  const computeOrigin = () => {
    const frame = frameRef.current
    if (frame === null) return "0px 0px"
    const frameH = frame.clientHeight 
    const frameW = frame.clientWidth
    return `${frameW/2 - dragOffset.x}px ${frameH/2 - dragOffset.y}px` 
  }

  return (
    <div className='image-canvas'>
      <Draggable
        onDrag = {(e, data) => {
          setDragOffset({x: data.x, y: data.y})
        }}
      >
        <div style={{filter:`brightness(${gain})`}}>
          <canvas 
            style={{transform: `scale(${zoom})`,
                  transformOrigin: computeOrigin(),
            }} 
            ref={canvasRef} 
            width={distance * cols} 
            height={distance * rows}
          />
        </div>
      </Draggable>
    </div>
  )
}
export default ImageCanvas
