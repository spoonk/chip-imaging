import React from 'react'
import { useRef, useEffect } from 'react'

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
 * @returns 
 */
const ImageCanvas = ({images, rows, cols, pixelsPerUM, theta, distance}) => {
    // note: for now, just use the same dimensions as expected by 
    // doing an actual stitching (with big pixels and stuff)
    // : because the canvas will eventually be pannable and zoomable
    const canvasRef = useRef(null)

    useEffect(() => {
        console.log("yo")
        const canvas = canvasRef.current
        const ctx = canvas.getContext('2d')

        // clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height)

        // generate a list of usable image elements
        const htmlImages = generateHTMLImages(images)

        // paste images into canvas

        const R =   [[Math.cos(theta), -Math.sin(theta)],
                     [Math.sin(theta), Math.cos(theta)]]

        console.log(htmlImages)
        htmlImages.forEach((image, index) => {
            // determine where to place image
            const row = Math.floor(index / cols) 
            const col = index % cols

            // convert to x,y pixel coordinates
            const pix_X = distance * col * pixelsPerUM
            const pix_Y = distance * row * pixelsPerUM

            const rotated = dotProduct(R, [pix_X, pix_Y])

            pasteImageIntoCanvas(image,rotated, ctx)
        })
        
    }, [images, rows, cols, pixelsPerUM, theta, distance]) // check dependencies later

    /**
     * returns a list of HTMLElement images
     * @param {*} images a list of base64 encoded images 
     */
    const generateHTMLImages = (images) => {
        return(
            images.map((image) => {
                const im = document.createElement('img');
                im.src = `data:image/png;base64, ${image}`
                im.alt= "microscope image"
                // document.body.appendChild(im)
                return im;
            })
        )
    }


    const pasteImageIntoCanvas = (image, pix_xy, ctx) => {
        // paste images into correct 
        console.log('?')
        ctx.drawImage(image, pix_xy[0], pix_xy[1]);
    }

    /**
     * computes the dot product Mv
     * @param {*} M 2 x 2 matrix
     * @param {*} v 1 x 2 vector
     * (I know dims don't match, just accept it)
     */
    const dotProduct = (M, v) => {
        return [
            v[0] * M[0][0] + v[1] * M[0][1],
            v[0] * M[1][0] + v[1] * M[1][1],
        ];
    }

  return (
    <div className='image-canvas'>
        <canvas ref={canvasRef} width={distance * cols} height={distance * rows}/>
    </div>
  )
}

export default ImageCanvas
            // map((url, index) => {
            // return(
            //     <img 
            //     src={"data:image/png;base64, " + url} 
            //     alt="camera feed frame" 
            //     key={index}
            //     />
            // )})