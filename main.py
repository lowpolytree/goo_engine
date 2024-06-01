import pyglet
from scenes.game_window_4 import GameWindow4

window = GameWindow4()
pyglet.clock.schedule_interval(window.update, 1/60.0)  # 60 fps
pyglet.app.run()
