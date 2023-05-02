/**
 * collection of functions to send messages to the server
 * 
 * abstracts away this communication from components
 */

import { serverUrl } from "./config"

export class ServerInterface {

    /**
     * pings the server for the status of the device,
     * returning a json object or None
     */
    static initialize = async() => {
        fetch(`${serverUrl}/initialize`)
    }

    /**
     * pings the server for the status of the device,
     * returning a json object or None
     */
    static getStatus = async() => {

    }

    static setGainExposure = async(gain, exposure) => {
        console.info(await fetch(`${serverUrl}/exposure/${exposure}`))
        console.info(await fetch(`${serverUrl}/gain/${gain}`))
    }

}