/**
 * collection of functions to send messages to the server
 * 
 * abstracts away this communication from components
 */
// TODO: document and standardize the server routes + responses

import { serverUrl } from "./config"

export class ServerInterface {
    // TODO: try catch for everything in case server offline

    /**
     * All functions return a 2-dimensional list of the form
     * [succeeded:bool, response:str]
     * A request will not succeed if the server is running 
     * but the device is unable to service the request
     */

    /**
     * pings the server for the status of the device,
     * returning a json object or None
     */
    static initialize = async() => {
        const initRes = await fetch(`${serverUrl}/initialize`)
        const text = await initRes.text()
        return [text==='initialized', text]
    }

    /**
     * pings the server for the status of the device,
     * returning [true, status] if the device is online
     */
    static getStatus = async() => {
        const result = await fetch(`${serverUrl}/status`)
        const text = await result.text()
        return [text!=='offline', text]
    }

    static setImagingParameters = async(width, height, distance) => {
        const setParamResult = await fetch(`${serverUrl}/update/${width}/${height}/${distance}`)
        const text = await setParamResult.text()
        return [text==='success', text]
    }

    static saveTopLeftPosition = async() => {
        const saveTopLeftResult = await fetch(`${serverUrl}/topLeft`)
        const text = await saveTopLeftResult.text()
        return [text ==='please initialize the device first']
    }

    static setGainExposure = async(gain, exposure) => {
        const exposureResult = await fetch(`${serverUrl}/exposure/${exposure}`)
        const gainResult = await fetch(`${serverUrl}/gain/${gain}`)
        // TODO: interpret if they worked
        return [exposureResult !== gainResult, [exposureResult, gainResult]]
    }

    static promptPath = async() => {
        const promptResult = await fetch(`${serverUrl}/promptDataPath`)
        const text = await promptResult.text()
        return [text!=='please initialize the device first' ,text]
    }

    static startStitching = async() => {
        const stitchRes = await fetch(`${serverUrl}/stitch`)
        const text = await stitchRes.text()
        return [text!=='please initialize the device first' ,text]
    }

    static acquire = async() => {
        const acqRes = await fetch(`${serverUrl}/acquire`)
        const text = await acqRes.text()
        return [text!=='please initialize the device first' ,text]
    }

    /**
     * Fetches a 3x3 grid of images representing the top left 3x3 image grid of the chip
     * If there aren't enough images for a 3x3, returns as many images as possible
     * (<9). If there are no images at all, success will be false
     */
    static getAlignmentGrid = async(h, w) => {
        const acqRes = await fetch(`${serverUrl}/manualGrid/${h}/${w}`)
        const alJson = await acqRes.json()
        console.log(alJson)
        return alJson
        // console.log(acqRes)
    }
}
