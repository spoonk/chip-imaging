import { io } from 'socket.io-client'
import { backendAddress } from './config'

export const socket = io(backendAddress)