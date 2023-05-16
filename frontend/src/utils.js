import { toast } from "react-toastify";

/**
 * takes in an array of [bool, message: str]
 * displaying a toast with the message
 */
const showToast = (result) => {
    if (result[0]) toast.success(result[1], {position:'bottom-left'})
    else toast.error(result[1], {position:'bottom-left'})
}

export { showToast }

