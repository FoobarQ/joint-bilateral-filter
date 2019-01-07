# The Joint Bilateral Filter

This is the programming section of my image processing submodule coursework. 

## How It Works
The filter works by:
1. taking two images- an ambient image, and a flash-photography image
2. applying the bilateral filter on the ambient image using the flash image's colour differences.

### From the commandline:
Images can be supplied as commandline arguments.
For the filter to work the way it's intended, the first image must be the ambient image, and the second flash.