todo:

[ x ] fix bug where first canvas draw doesn't render
    - wasn't a bug lol, just slow
[ x ] get draggable canvas working
[ x ] make canvas zoomable
[ x ] integrate material ui stuff for ui
    [ x ] buttons
    [ x ] number inputs
    - traverse from top down to replace buttons

[ x ] refactor imaging canvas so we can have controls on the canvas area
[ x ] have sliders for theta (use input instead)
[ x ] have canvas controls overlap the actual canvas to save space
[ x ] crop canvas component


[ x ] * make mocks of all devices for testing on mac / linux

[ x ] websockets, not flask -> better streaming + flask is annoying with warning
    [ ] might want to refactor camera for continuous acquisition, storing image in a buffer and 
        accessing that buffer rather than resnapping each time (super slow)

[ ] full server integration
    [ x ] make all routes nice + toasted
    [ ] make sure all errors are handled (not sure if this is every checkable)

[ x ] better image saving
    [ x ] check to make sure directory is empty
    [ x ] make a directory just for the raw images
        [ x ] stores an imaging grid config as well
    [ x ] in parent of raw image dir, save stitch
    [ x ] test on pc that doesn't crash with tkinger :|

    so we have something like 
    -session
    |- raw_images
     |- *.Tiff
    |-stitched.tiff

[ x ] server rejects a path if it is a non empty directory
[ x ] use different websockets for (hopefully) better streaming -> just use gevent
[ x ] put manual alignmnet into stitching menu, get rid of manual alignt menu
[ x ] make camera feed toggleable

[ x ] toastify for alerts (fetching stuff)
[ x ] interpret return values from manager
[ x ] route to query the path that images will be saved in

[ ] separate the imaging and stitching paths, providing an option to stitch in the acquisition directory
    - you might want to stitch in an existing data dir
[ ] manager better return messages / types



[ ] make manual align send a theta to the server
[ ] also send a pixels per um
[ ] make linear stitcher be able to handle a rotation
[ ] make stitcher able to handle fewer than expected images (it might already)

[ ] make querying the manual grid depend on stitcher's path
[ ] server offline errors for request

[ ] implement getting stitched result

[ ] make manual grid route respect imaging grid parameters
    - currently just sends a 3x3, we want to handle the case where there may not be a 3x3 to return

[ ] clean up server routes with blueprints

[ ] documentation
[ ] way to kill / restart server devices

[ ] make a stitch utils file in python that allows you to get jpeg images (for sending manual grid back to client)
    [ ] also need a gain scalar on frontend (images will likely be black)


[ ] zoom slider for manual align

[ ] figure out how to run server and frontend with exe file


[ ] add documentation on the website to say what each button means (popup or something)


[ ] stitching stuff needs to not require device to be initialized

