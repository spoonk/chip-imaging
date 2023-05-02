import { io } from 'socket.io-client'
import { serverUrl } from './config'

export const socket = io(serverUrl)