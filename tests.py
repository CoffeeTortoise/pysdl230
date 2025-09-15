from pysdl2.LoadDLL import LoadDLL, TTFDLL, ImageDLL, MixerDLL
LoadDLL.DLL_PATH = 'SDL2bins/SDL2.dll'
TTFDLL.DLL_PATH = 'SDL2bins/SDL2_ttf.dll'
ImageDLL.DLL_PATH = 'SDL2bins/SDL2_image.dll'
MixerDLL.DLL_PATH = 'SDL2bins/SDL2_mixer.dll'
LoadDLL.load_dll()
MixerDLL.load_dll()
ImageDLL.load_dll()
TTFDLL.load_dll()


from pysdl2.SDL_timer import SDL_Delay
from pysdl2.SDL_pixels import SDL_Color
from pysdl2.SDL_keycode import SDL_KeyCode
from pysdl2.SDL_scancode import SDL_Scancode
from pysdl2.SDL_keyboard import SDL_GetKeyboardState
from pysdl2.SDL_rect import SDL_Rect, SDL_HasIntersection
from pysdl2.SDL import SDL_Init, SDL_INIT_EVERYTHING, SDL_Quit
from pysdl2.SDL_mouse import SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT
from pysdl2.SDL_events import SDL_Event, SDL_PollEvent, SDL_EventType
from pysdl2.SDL_video import SDL_GetDesktopDisplayMode, SDL_DisplayMode
from pysdl2.SDL_video import SDL_CreateWindow, SDL_DestroyWindow, SDL_WindowFlags, SDL_WINDOWPOS_CENTERED
from pysdl2.SDL_image import IMG_InitFlags, IMG_Init, IMG_Quit, IMG_LoadTexture, IMG_Load
from pysdl2.SDL_render import SDL_DestroyRenderer, SDL_CreateRenderer, SDL_RendererFlags, SDL_RenderCopy
from pysdl2.SDL_render import SDL_SetRenderDrawColor, SDL_RenderClear, SDL_RenderPresent, SDL_RenderFillRect
from pysdl2.SDL_render import SDL_DestroyTexture, SDL_RenderCopyEx, SDL_RendererFlip, SDL_QueryTexture
# import pysdl2.sdl2

import ctypes
import sys
import os


def draw_rect(renderer, rect, clr):
	SDL_SetRenderDrawColor(renderer, clr.r, clr.g, clr.b, clr.a)
	SDL_RenderFillRect(renderer, ctypes.byref(rect))


def move_rect(rect, dx, dy):
	rect.x += dx
	rect.y += dy


class Sprite:
	
	def __init__(self,
		renderer, img_path,
		width, height,
		left, top
		):
		self.texture = IMG_LoadTexture(renderer, img_path)		# It's better to create texture from surface, but whatever
		self.rect = SDL_Rect()
		self.rect.w, self.rect.h = width, height
		self.rect.x, self.rect.y = left, top
	
	def draw(self, renderer):
		SDL_RenderCopyEx(renderer, self.texture, None, ctypes.byref(self.rect), 0, None, SDL_RendererFlip.SDL_FLIP_HORIZONTAL)
		# SDL_RenderCopy(renderer, self.texture, None, ctypes.byref(self.rect))
	
	def __del__(self):
		SDL_DestroyTexture(self.texture)


class Animation:
	
	def __init__(self,
		renderer, img_paths,
		width, height,
		left, top, speed
		):
			self.speed = speed
			self.cntr = 0
			self.sprites = [Sprite(renderer, path, width, height, left, top) for path in img_paths]
	
	def draw(self, renderer):
		ind = int(self.cntr)
		if ind >= len(self.sprites):
			self.cntr = 0
			ind = 0
		self.sprites[ind].draw(renderer)
		self.cntr += self.speed


def main():
	mode = SDL_DisplayMode()
	SDL_GetDesktopDisplayMode(0, ctypes.byref(mode))
	width, height = int(mode.w * .8), int(mode.h * .8)
	wnd = SDL_CreateWindow(
		'Some tests',	   # Note: python27 byte str
		SDL_WINDOWPOS_CENTERED,
		SDL_WINDOWPOS_CENTERED,
		width, height,
		SDL_WindowFlags.SDL_WINDOW_SHOWN | SDL_WindowFlags.SDL_WINDOW_RESIZABLE
	)
	renderer = SDL_CreateRenderer(wnd, -1, SDL_RendererFlags.SDL_RENDERER_ACCELERATED)
	red, green, blue, grey = SDL_Color(), SDL_Color(), SDL_Color(), SDL_Color()
	red.r, green.r, blue.r, grey.r = 255, 0, 0, 128
	red.g, green.g, blue.g, grey.g = 0, 255, 0, 128
	red.b, green.b, blue.b, grey.b = 0, 0, 255, 128
	red.a, green.a, blue.a, grey.a = 255, 255, 255, 255
	black, white = SDL_Color(), SDL_Color()
	black.r, black.g, black.b, black.a = 0, 0, 0, 255
	white.r, white.g, white.b, white.a = 255, 255, 255, 255
	evt = SDL_Event()
	bg_clr = grey
	running, delay = True, 16
	
	img_folder = 'assets/Bird'
	img_paths = [os.path.join(img_folder, img_name) for img_name in os.listdir(img_folder)]
	anim_w, anim_h = int(height * .3), int(height * .3)
	anim_x, anim_y = int(width * .3), int(height * .3)
	anim_speed = .15
	anim = Animation(renderer, img_paths, anim_w, anim_h, anim_x, anim_y, anim_speed)
	
	rect1, rect2 = SDL_Rect(), SDL_Rect()
	rect1.w, rect2.w = int(width * .25), int(width * .25)
	rect1.h, rect2.h = int(height * .333), int(height * .333)
	rect1.x, rect2.x = 0, width - rect2.w
	rect1.y, rect2.y = int(height * .5 - rect1.h * .5), int(height * .5 - rect2.h * .5)
	rect_speed = int(width * .01)
	
	while running:
		while SDL_PollEvent(ctypes.byref(evt)):
			if evt.type == SDL_EventType.SDL_QUIT:
				running = False
			elif evt.type == SDL_EventType.SDL_KEYDOWN:
				key = evt.key.keysym.sym
				if key == SDL_KeyCode.SDLK_d:
					move_rect(rect1, rect_speed, 0)
				elif key == SDL_KeyCode.SDLK_a:
					move_rect(rect1, -rect_speed, 0)
			elif evt.type == SDL_EventType.SDL_MOUSEBUTTONDOWN:
				btn = evt.button.button
				if btn == SDL_BUTTON_LEFT:
					bg_clr = white
				elif btn == SDL_BUTTON_RIGHT:
					bg_clr = black
				else:
					bg_clr = grey
		
		kb_state = SDL_GetKeyboardState(None)
		if kb_state[SDL_Scancode.SDL_SCANCODE_W]:
			move_rect(rect2, 0, -rect_speed)
		if kb_state[SDL_Scancode.SDL_SCANCODE_S]:
			move_rect(rect2, 0, rect_speed)
		
		SDL_SetRenderDrawColor(renderer, bg_clr.r, bg_clr.g, bg_clr.b, bg_clr.a)
		SDL_RenderClear(renderer)
		
		rect1_clr, rect2_clr = red, blue
		if SDL_HasIntersection(ctypes.byref(rect1), ctypes.byref(rect2)):
			rect1_clr, rect2_clr = blue, red
		draw_rect(renderer, rect1, rect1_clr)
		draw_rect(renderer, rect2, rect2_clr)
		
		anim.draw(renderer)
		SDL_RenderPresent(renderer)
		SDL_Delay(delay)
	
	SDL_DestroyRenderer(renderer)
	SDL_DestroyWindow(wnd)


if __name__ == '__main__':
	if sys.platform.startswith('win'):
		ctypes.windll.user32.SetProcessDPIAware()
	sys.stdout.write('start!\n')
	SDL_Init(SDL_INIT_EVERYTHING)
	IMG_Init(IMG_InitFlags.IMG_INIT_PNG)
	main()
	IMG_Quit()
	SDL_Quit()
	sys.stdout.write('end!\n')