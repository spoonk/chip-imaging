/**
 * collection of functions to send messages to the server
 * 
 * abstracts away this communication from components
 */
// TODO: document and standardize the server routes + responses

import { serverUrl } from "./config"

export class ServerInterface {
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
    const body = await initRes.json()
    return body 
  }

  /**
   * pings the server for the status of the device,
   * returning [true, status] if the device is online
   */
  static getStatus = async() => {
    const result = await fetch(`${serverUrl}/status`)
    const body = await result.json()
    return body
  }

  static setImagingParameters = async(width, height, distance) => {
    const setParamResult = await fetch(`${serverUrl}/update/${width}/${height}/${distance}`)
    const body = await setParamResult.json()
    return body
  }

  static saveTopLeftPosition = async() => {
    const saveTopLeftResult = await fetch(`${serverUrl}/topLeft`)
    const body = await saveTopLeftResult.json()
    return body
  }

  static setGainExposure = async(gain, exposure) => {
    const exposureResult = await fetch(`${serverUrl}/exposure/${exposure}`)
    const ebody = await exposureResult.json()

    const gainResult = await fetch(`${serverUrl}/gain/${gain}`)
    const gbody = await gainResult.json()

    return [ebody[0] && gbody[0], JSON.stringify(ebody[1]) + " " + JSON.stringify(gbody[1])]
  }

  static promptPath = async() => {
    const promptResult = await fetch(`${serverUrl}/promptDataPath`)
    return await promptResult.json()
  }

  static startStitching = async() => {
    const stitchRes = await fetch(`${serverUrl}/stitch`)
    return await stitchRes.json()
  }

  static acquire = async() => {
    const acqRes = await fetch(`${serverUrl}/acquire`)
    return await acqRes.json()
  }

  /**
     * Fetches a 3x3 grid of images representing the top left 3x3 image grid of the chip
     * If there aren't enough images for a 3x3, returns as many images as possible
     * (<9). If there are no images at all, success will be false
     */
  static getAlignmentGrid = async(h, w) => {
    const acqRes = await fetch(`${serverUrl}/manualGrid/${h}/${w}`)
    const alJson = await acqRes.json()
    return alJson
  }


  static promptStitchingPath = async() => {
    const promptResult = await fetch(`${serverUrl}/promptStitchingPath`)
    return await promptResult.json()
  }
}
