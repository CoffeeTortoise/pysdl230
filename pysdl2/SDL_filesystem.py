import ctypes


SOME.SDL_GetBasePath.restype = ctypes.c_char_p
SOME.SDL_GetBasePath.argtypes = []

def SDL_GetBasePath():
	"""
	Args:
		: None.
	Returns:
		res: ctypes.c_char_p.
	"""
	return SOME.SDL_GetBasePath()


SOME.SDL_GetPrefPath.restype = ctypes.c_char_p
SOME.SDL_GetPrefPath.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

def SDL_GetPrefPath(org, app):
	"""
	Args:
		org: ctypes.c_char_p.
		app: ctypes.c_char_p.
	Returns:
		res: ctypes.c_char_p.
	"""
	return SOME.SDL_GetPrefPath(org, app)