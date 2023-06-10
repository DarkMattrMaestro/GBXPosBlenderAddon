# GBXPosBlenderAddon

*Disclaimer 1: This repository is a complete mess*

*Disclaimer 2: This project is still in early development, and therefore is incomplete and full of bugs*

## About

GBXPos is a Blender addon that lets you import TMNF/TMUF replays into Blender. It is mainly meant to be a video editing tool, making compositing 3D and 2D objects into a replay (after the render) easier.

Here is an example of something that can be done with the addon: https://www.youtube.com/watch?v=qR4xeBVV2Js

## Features

- Loading *some* camera movement
- Loading blocks
- Loading the ghost and it's movement
- Compositing the render on top of the replay

## Incomplete

- Camera animation
  - Hermite & Fixed Tangant interpolation aren't yet added
  - Anything other than the Custom Camera doesn't work
- Textures
  - The transparency textures for the ghost and blocks is not complete
- Ghosts
  - Only one ghost is supported
  - The pivot point for the car might be wrong
- And more...

## *Hopefully* Future Features

- Proper suspension for the ghost
- Exporting camera motion from Blender to the GBX file
- Cycles & Eevee support (currently only using Eevee)
- A key to quickly add a preset text object on the face of the object you click on (to make adding text in 3D fast)
- Readable code (This feature may be impossible)
