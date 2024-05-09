import pyglet
from scenes.game_window_3 import GameWindow3

window = GameWindow3()
pyglet.clock.schedule_interval(window.update, 1/60.0)  # 60 fps
pyglet.app.run()
