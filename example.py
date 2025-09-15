from pysdl2.LoadDLL import LoadDLL, TTFDLL, ImageDLL, MixerDLL
LoadDLL.DLL_PATH = 'SDL2bins/SDL2.dll'
TTFDLL.DLL_PATH = 'SDL2bins/SDL2_ttf.dll'
ImageDLL.DLL_PATH = 'SDL2bins/SDL2_image.dll'
MixerDLL.DLL_PATH = 'SDL2bins/SDL2_mixer.dll'
LoadDLL.load_dll()
MixerDLL.load_dll()
ImageDLL.load_dll()
TTFDLL.load_dll()


import ctypes
import sys
from pysdl2.SDL_rect import SDL_Rect
from pysdl2.SDL_timer import SDL_Delay
from pysdl2.SDL_pixels import SDL_Color
from pysdl2.SDL_surface import SDL_FreeSurface
from pysdl2.SDL import SDL_Init, SDL_INIT_EVERYTHING, SDL_Quit
from pysdl2.SDL_events import SDL_Event, SDL_PollEvent, SDL_EventType
from pysdl2.SDL_video import SDL_GetDesktopDisplayMode, SDL_DisplayMode
from pysdl2.SDL_ttf import TTF_Init, TTF_Quit, TTF_OpenFont, TTF_RenderText_Solid, TTF_CloseFont
from pysdl2.SDL_render import SDL_SetRenderDrawColor, SDL_RenderClear, SDL_RenderPresent
from pysdl2.SDL_image import IMG_InitFlags, IMG_Init, IMG_Quit, IMG_LoadTexture, IMG_Load
from pysdl2.SDL_video import SDL_CreateWindow, SDL_DestroyWindow, SDL_SetWindowIcon, SDL_WindowFlags, SDL_WINDOWPOS_CENTERED
from pysdl2.SDL_render import SDL_DestroyRenderer, SDL_CreateRenderer, SDL_RendererFlags, SDL_RenderCopy, SDL_DestroyTexture
from pysdl2.SDL_render import SDL_CreateTextureFromSurface, SDL_QueryTexture
from pysdl2.SDL_mixer import MIX_InitFlags, Mix_Init, Mix_Quit, Mix_OpenAudio, MIX_DEFAULT_FORMAT, MIX_DEFAULT_FREQUENCY
from pysdl2.SDL_mixer import MIX_DEFAULT_CHANNELS, Mix_CloseAudio, Mix_FreeMusic, Mix_PlayMusic, MIX_DEFAULT_CHUNKSIZE, Mix_LoadMUS


def main():
    mode = SDL_DisplayMode()
    if SDL_GetDesktopDisplayMode(0, ctypes.byref(mode)):
        sys.stderr.write('Failed to get resolution!\n')
        IMG_Quit()
        TTF_Quit()
        Mix_Quit()
        SDL_Quit()
        sys.exit()
    sys.stdout.write('Resolution: {}x{}\n'.format(mode.w, mode.h))
    width, height = int(mode.w * .5), int(mode.h * .666)
    wnd = SDL_CreateWindow(
        'SDL_test',                # Note: python27 byte str
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        width, height,
        SDL_WindowFlags.SDL_WINDOW_SHOWN | SDL_WindowFlags.SDL_WINDOW_RESIZABLE
    )
    if not wnd:
        sys.stderr.write('Failed to create window!\n')
        IMG_Quit()
        TTF_Quit()
        Mix_Quit()
        SDL_Quit()
        sys.exit()
    renderer = SDL_CreateRenderer(wnd, -1, SDL_RendererFlags.SDL_RENDERER_ACCELERATED)
    if not renderer:
        sys.stderr.write('Failed to create renderer!\n')
        SDL_DestroyWindow(wnd)
        IMG_Quit()
        TTF_Quit()
        Mix_Quit()
        SDL_Quit()
        sys.exit()
    icon_path = 'assets/python.png'
    icon = IMG_Load(icon_path)
    if not icon:
        sys.stderr.write('Failed to load {}!\n'.format(icon_path))
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(wnd)
        IMG_Quit()
        Mix_Quit()
        TTF_Quit()
        SDL_Quit()
        sys.exit()
    SDL_SetWindowIcon(wnd, icon)
    SDL_FreeSurface(icon)
    
    cof_image = 'assets/coffee.png'
    cof_texture = IMG_LoadTexture(renderer, cof_image)
    if not cof_texture:
        sys.stderr.write('Failed to load {}!\n'.format(cof_image))
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(wnd)
        IMG_Quit()
        TTF_Quit()
        SDL_Quit()
        Mix_Quit()
        sys.exit()
    cof_rect = SDL_Rect()
    cof_rect.w, cof_rect.h = int(width * .9), height
    cof_rect.x, cof_rect.y = 0, 0
    
    fnt_path, fnt_size = 'assets/cyrillicolda_bold.ttf', int(height * .1)
    fnt = TTF_OpenFont(fnt_path, fnt_size)
    if not fnt:
        sys.stderr.write('Failed to load {}!\n'.format(fnt_path))
        SDL_DestroyTexture(cof_texture)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(wnd)
        IMG_Quit()
        TTF_Quit()
        Mix_Quit()
        SDL_Quit()
        sys.exit()
    fnt_clr = SDL_Color()
    fnt_clr.r, fnt_clr.g, fnt_clr.b, fnt_clr.a = 0, 0, 0, 255
    text_surface = TTF_RenderText_Solid(fnt, 'Font works!', fnt_clr)
    if not text_surface:
        sys.stderr.write('Failed to create surface for text!\n')
        TTF_CloseFont(fnt)
        SDL_DestroyTexture(cof_texture)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(wnd)
        IMG_Quit()
        Mix_Quit()
        TTF_Quit()
        SDL_Quit()
        sys.exit()
    text_texture = SDL_CreateTextureFromSurface(renderer, text_surface)
    SDL_FreeSurface(text_surface)
    text_w, text_h = ctypes.c_int(0), ctypes.c_int(0)
    SDL_QueryTexture(text_texture, None, None, ctypes.byref(text_w), ctypes.byref(text_h))
    txt_rect = SDL_Rect()
    txt_rect.w, txt_rect.h = text_w, text_h
    txt_rect.x, txt_rect.y = int(width * .5 - text_w.value * .5), height - text_h.value * 3
    
    if Mix_OpenAudio(MIX_DEFAULT_FREQUENCY, MIX_DEFAULT_FORMAT, MIX_DEFAULT_CHANNELS, MIX_DEFAULT_CHUNKSIZE) < 0:
        sys.stderr.write('Failed to initialize mixer!\n')
        TTF_CloseFont(fnt)
        SDL_DestroyTexture(text_texture)
        SDL_DestroyTexture(cof_texture)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(wnd)
        IMG_Quit()
        Mix_Quit()
        TTF_Quit()
        SDL_Quit()
        sys.exit()
    mus_path = 'assets/sunset.ogg'
    mus = Mix_LoadMUS(mus_path)
    if not mus:
        sys.stderr.write('Failed to load music!\n')
        TTF_CloseFont(fnt)
        Mix_CloseAudio()
        SDL_DestroyTexture(text_texture)
        SDL_DestroyTexture(cof_texture)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(wnd)
        IMG_Quit()
        Mix_Quit()
        TTF_Quit()
        SDL_Quit()
        sys.exit()
    if Mix_PlayMusic(mus, -1) == -1:
        sys.stderr.write('Failed to play music!\n')
        TTF_CloseFont(fnt)
        Mix_FreeMusic(mus)
        Mix_CloseAudio()
        SDL_DestroyTexture(text_texture)
        SDL_DestroyTexture(cof_texture)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(wnd)
        IMG_Quit()
        Mix_Quit()
        TTF_Quit()
        SDL_Quit()
        sys.exit()
    
    bg_clr = SDL_Color()
    bg_clr.r, bg_clr.g, bg_clr.b, bg_clr.a = 120, 219, 226, 255
    running, delay = True, 16
    evt = SDL_Event()
    while running:
        while SDL_PollEvent(ctypes.byref(evt)):
            if evt.type == SDL_EventType.SDL_QUIT:
                running = False
        SDL_SetRenderDrawColor(renderer, bg_clr.r, bg_clr.g, bg_clr.b, bg_clr.a)
        SDL_RenderClear(renderer)
        SDL_RenderCopy(renderer, cof_texture, None, ctypes.byref(cof_rect))
        SDL_RenderCopy(renderer, text_texture, None, ctypes.byref(txt_rect))
        SDL_RenderPresent(renderer)
        SDL_Delay(delay)
    SDL_DestroyTexture(text_texture)
    SDL_DestroyTexture(cof_texture)
    SDL_DestroyRenderer(renderer)
    SDL_DestroyWindow(wnd)
    TTF_CloseFont(fnt)
    Mix_FreeMusic(mus)
    Mix_CloseAudio()
    IMG_Quit()
    Mix_Quit()
    TTF_Quit()
    SDL_Quit()


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        ctypes.windll.user32.SetProcessDPIAware()
    sys.stdout.write('start!\n')
    SDL_Init(SDL_INIT_EVERYTHING)
    IMG_Init(IMG_InitFlags.IMG_INIT_PNG)
    Mix_Init(MIX_InitFlags.MIX_INIT_OGG)
    TTF_Init()
    main()
    sys.stdout.write('end!')