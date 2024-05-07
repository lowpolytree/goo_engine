import pyglet
from scenes.game_window_1 import GameWindow1
from scenes.game_window_2 import GameWindow2

window = GameWindow2()
pyglet.clock.schedule_interval(window.update, 1/60.0)  # 60 fps
pyglet.app.run()
