from pyglet.window import key
from entity import Entity
from scenes.scene_base import Scene
from components.components import *
from systems.systems import *
from utils.spring import Spring

# showcasing anchor springs

class GameWindow4(pyglet.window.Window):
    def __init__(self):
        super().__init__(1280, 720)

        self.fps_display = pyglet.window.FPSDisplay(self)

        self.batch = pyglet.graphics.Batch()  # Create a batch for drawing
        self.scene = Scene()  # Initialize the scene
        self.physics_system = PhysicsSystem()
        self.springs = ()
        self.setup_scene()
        
    def setup_scene(self):

        s1 = Spring((600, 600), (600, 200), 7.0, 250, self.batch)
        s1.add_to_scene(self.scene, self.physics_system)

        s2 = Spring((300, 600), (300, 300), 5.0, 350, self.batch)
        s2.add_to_scene(self.scene, self.physics_system)

        s3 = Spring((900, 600), (900, 250), 5.0, 200, self.batch)
        s3.add_to_scene(self.scene, self.physics_system)

        self.springs = (s1, s2, s3)
        self.scene.add_system(self.physics_system)

    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        self.batch.draw()  # Draw everything in the batch

    def update(self, dt):
        self.scene.update(dt)

        for s in self.springs:
            s.update(dt)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            pass

