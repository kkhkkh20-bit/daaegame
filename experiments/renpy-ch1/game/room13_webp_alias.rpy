# The web package stores active pixel art as lossless WebP (dev/package_web_webp.py)
# and deletes the PNG. Saves made before that may still hold "room13-pixel-*.png"
# paths; serve the WebP twin. Source builds ship no twin and never reach it.
# pygame.image.load detects PNG/WebP by magic bytes, so the .png hint is harmless.
init -100 python:
    def r13_webp_twin(name):
        if "room13-pixel-" in name and name.endswith(".png"):
            twin=name[:-4]+".webp"
            if renpy.loader.loadable_core(twin):
                return twin
        return None

    _r13_webp_previous_open=config.file_open_callback

    def r13_webp_open(name):
        twin=r13_webp_twin(name)
        if twin:return renpy.loader.load_core(twin)
        return _r13_webp_previous_open(name) if _r13_webp_previous_open else None

    config.loadable_callback=lambda name:r13_webp_twin(name) is not None
    config.file_open_callback=r13_webp_open
