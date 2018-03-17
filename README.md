# SPACE MADNESS
This game was created during Yelp's Hackathon 25. Here's a video:

[![Space Madness Video](https://img.youtube.com/vi/7qCSeqjKI3c/0.jpg)](https://www.youtube.com/watch?v=7qCSeqjKI3c)

# INSTALL
**NOTE: these instructions were tested exclusively on MacOS**

## Install system dependencies and libraries

* Install the support for the XBOX360 controllers following the instructions [here](https://github.com/360Controller/360Controller/releases)
* Download SDL2 from [this download page](https://www.libsdl.org/download-2.0.php)
* The installer contains `SDL2.Framework` inside. Move it to `/Library/Frameworks`
* Make sure you have python **3.6** installed. See [the official download page](https://www.python.org/downloads/) (or use `brew`)
* Install `swig` with `brew install swig`

## Download and install code requirements

* Clone SpaceMadness repo:
    git clone git@github.com:maxfish/SpaceMadness.git
* cd `SpaceMadness`
* Create a new virtualenv: `python3.6 -m venv venv`
* Activate it: `venv/bin/activate`
* Get `pybox2d` by cloning it (git clone https://github.com/pybox2d/pybox2d) or downloading it (`curl -o pybox2d.zip https://codeload.github.com/pybox2d/pybox2d/zip/master && unzip pybox2d.zip`) within the game folder
* Build `pybox2d`: `cd pybox2d && python setup.py build && python setup.py develop && cd ..`
* Install the requirements: `pip install -r requirements.txt`

## Hardware requirements

* **OpenGL**: The game requires OpenGL v4.1 (core profile)
* **Joysticks**: You will need 3 joypads to control each single ship. The joysticks handling is done via SDL2 but right now only XBox360 and PS4 controller are supported. To support more joysticks models, or another OS, please have a look at the SDL2 database here: https://github.com/gabomdq/SDL_GameControllerDB

RUN
===

    $ python game.py
    $ python game.py --width=1000 --height=800 (custom width/height)
