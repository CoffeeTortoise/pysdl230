# SDL2 ctypes Wrapper for Python

This is a wrapper for the SDL2 library for Python, implemented using ctypes. It supports both Python 2 and Python 3.

## Description

SDL (Simple DirectMedia Layer) is a library that provides low-level access to audio, keyboard, mouse, joystick, and graphics through OpenGL and Direct3D. This wrapper allows you to use SDL2 in Python, providing a simple and convenient interface for multimedia applications.

## Installation

### Dependencies

Before installation, ensure you have the following dependencies:

- Python 2.x or 3.x
- SDL2 library

### Installing SDL2

On Ubuntu and Mint, you can install SDL2 using the following command:

```bash
sudo apt update
sudo apt install libsdl2-dev
sudo apt install libsdl2-ttf-dev
sudo apt install libsdl2-mixer-dev
sudo apt install libsdl2-image-dev
```

### Installing pysdl230

```
pip install pysdl230-0.1-py2-none-any.whl
```
Or:
```
pip install pysdl230-0.1-py3-none-any.whl
```
Or just:
```
pip install pysdl230
```

## Documentation

This wrapper is very low-level. Therefore, what applies to SDL2 will be true for the most part.
SDL2 documentation: [SDL2/FrontPage](https://wiki.libsdl.org/SDL2/FrontPage)
Also recommend: [SDL2.0 tutorial](https://kleinbauer.fr/alexis/ebook/SDL_Game_Development_en.pdf)

## Feedback

Found some issues? Please, contact me: e.8ychkov@yandex.ru