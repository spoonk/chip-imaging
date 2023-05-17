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

[ ] better image saving
    [ ] make a directory just for the raw images
        [ ] stores an imaging grid config as well
    [ ] in parent of raw image dir, save stitch

    so we have something like 
    -session
    |- raw_images
     |- *.Tiff
    |-stitched.tiff

[ ] make manual align send a theta to the server
[ ] make linear stitcher be able to handle a rotation

[ ] make querying the manual grid depend on path

[ ] make camera feed toggleable

[ ] toastify for alerts (fetching stuff)
[ ] override onscroll for image canvas -> so canvas gets scrolled
[ ] use different websockets for (hopefully) better streaming
[ ] make manual grid route respect imaging grid parameters


[ ] clean up server routes with blueprints

[ ] documentation
[ ] way to kill / restart server devices

[ ] server rejects a path if it is a non empty directory
[ ] route to query the path that images will be saved in
[ ] make a stitch utils file in python that allows you to get jpeg images 
[ ] be able to select a different directory for stiching, not just the one from acquisition

[ ] interpret return values from manager
