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
    try{
      const initRes = await fetch(`${serverUrl}/initialize`)
      const body = await initRes.json()
      return body 
    } catch (e) {
      return [false, 'server offline']
    }
  }

  /**
   * pings the server for the status of the device,
   * returning [true, status] if the device is online
   */
  static getStatus = async() => {
    try{
      const result = await fetch(`${serverUrl}/status`)
      const body = await result.json()
      return body
    } catch (e) {
      return [false, 'server offline']
    }
  }

  static setImagingParameters = async(width, height, distance) => {
    try{
      const setParamResult = await fetch(`${serverUrl}/update/${width}/${height}/${distance}`)
      const body = await setParamResult.json()
      return body
    } catch (e) {
      return [false, 'server offline']
    }
  }

  static saveTopLeftPosition = async() => {
    try{
      const saveTopLeftResult = await fetch(`${serverUrl}/topLeft`)
      const body = await saveTopLeftResult.json()
      return body
    } catch (e) {
      return [false, 'server offline']
    }
  }

  static setGainExposure = async(gain, exposure) => {
    try{
      const exposureResult = await fetch(`${serverUrl}/exposure/${exposure}`)
      const ebody = await exposureResult.json()

      const gainResult = await fetch(`${serverUrl}/gain/${gain}`)
      const gbody = await gainResult.json()

      return [ebody[0] && gbody[0], JSON.stringify(ebody[1]) + " " + JSON.stringify(gbody[1])]
    } catch (e) {
      return [false, 'server offline']
    }
  }

  static promptPath = async() => {
    try{
      const promptResult = await fetch(`${serverUrl}/promptDataPath`)
      return await promptResult.json()
    } catch (e) {
      return [false, 'server offline']
    }
  }

  static startStitching = async() => {
    try{
      const stitchRes = await fetch(`${serverUrl}/stitch`)
      return await stitchRes.json()
    } catch (e) {
      return [false, 'server offline']
    }
  }

  static acquire = async() => {
    try{
      const acqRes = await fetch(`${serverUrl}/acquire`)
      return await acqRes.json()
    } catch (e) {
      return [false, 'server offline']
    }
  }

  /**
     * Fetches a 3x3 grid of images representing the top left 3x3 image grid of the chip
     * If there aren't enough images for a 3x3, returns as many images as possible
     * (<9). If there are no images at all, success will be false
     */
  static getAlignmentGrid = async(h, w) => {
    try{
      const gridRes = await fetch(`${serverUrl}/manualGrid/${h}/${w}`)
      const gridJson = await gridRes.json()
      return gridJson
    } catch (e) {
      return [false, 'server offline']
    }
  }


  static promptStitchingPath = async() => {
    try{
      const promptResult = await fetch(`${serverUrl}/promptStitchingPath`)
      return await promptResult.json()
    } catch (e) {
      return [false, 'server offline']
    }
  }

  static setStitchingParameters = async(theta, pixePerUm) => {
    try{
      const setResult = await fetch(`${serverUrl}/setStitchingParameters/${theta}/${pixePerUm}`)
      return await setResult.json()
    } catch (e) {
      return [false, 'server offline']
    }

  }
}
