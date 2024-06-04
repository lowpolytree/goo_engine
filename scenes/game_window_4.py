from pyglet.window import key
from math import sqrt
from entity import Entity
from scenes.scene_base import Scene
from components.components import *
from systems.systems import *
from utils.spring import AnchoredSpring, DoubleSpring

# showcasing anchor springs

class GameWindow4(pyglet.window.Window):
    def __init__(self):
        super().__init__(1280, 720)
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.batch = pyglet.graphics.Batch()  # Create a batch for drawing
        self.scene = Scene()  # Initialize the scene
        self.physics_system = PhysicsSystem()
        self.springs = ()
        self.pause_physics = False
        self.is_colliding = False
        self.setup_scene()
        
    def setup_scene(self):

        # s1 = DoubleSpring((600, 500), (600, 300), 10.0, 150, self.batch)
        # s1.add_to_scene(self.scene, self.physics_system)

        s2 = AnchoredSpring((300, 600), (300, 300), 10.0, 300.0, 0.97, self.batch)
        s2.add_to_scene(self.scene, self.physics_system)

        # s3 = AnchoredSpring((900, 600), (900, 250), 5.0, 200, self.batch)
        # s3.add_to_scene(self.scene, self.physics_system)

        self.springs = (s2,)
        self.scene.add_system(self.physics_system)

    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        self.batch.draw()  # Draw everything in the batch

    def update(self, dt):
        if not self.pause_physics:
            self.scene.update(dt)

        for s in self.springs:
            s.update(dt)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.pause_physics = True
            shape = self.springs[0].end_entity.get_component(ShapeComponent)
            if self.point_in_circle(x, y, shape.shape.position, 10.0):
                self.is_colliding = True
            
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons and pyglet.window.mouse.LEFT:
            if self.is_colliding:
                shape = self.springs[0].end_entity.get_component(ShapeComponent)
                shape.shape.position = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.is_colliding = False
            self.pause_physics = False        


    def point_in_circle(self, x, y, center, radius):
        # Calculate the distance from the point to the circle's center
        dist = sqrt((center[0] - x) ** 2 + (center[1] - y) ** 2)
        return dist <= radius