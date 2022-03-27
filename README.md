# donaty-app
Slicing project for bang [Andre Rio]( https://github.com/andregans )'s ui design.

## Requirements
- python > 3.6
- kivy > 2.0.0
- pyjnius
(pip install `requirements.txt` to install all of the packages required)

## Issues
This app using kivy `multisamples = 0` to avoid OpenGL 2.0 not detected error on some machines
even the machine have supported openGL version already.
It should be run properly in most machines that have error on the OpenGL version.

Some machines may be don't work with that method. But, you can try another way
to avoid the OpenGL error. You can add this lines of code to `main.py` file.
```
import os
os.environ[KIVY_GL_BACKEND] = 'angle_sdl2'
```
Using `multisamples = 0` or angle_sdl2 for KIVY_GL_BACKEND can increase performance of
the app if the app have so many animation and events. but it also reduce the graphic
quality for some elements.
