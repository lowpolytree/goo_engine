from pyglet.window import key
import random
from math import cos, sin, pi
from entity import Entity
from scenes.scene_base import Scene
from components.components import *
from systems.systems import *

#spawns a bullet with a mouse press
#bullet factory function

class GameWindow2(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 600)
        self.batch = pyglet.graphics.Batch()  # Create a batch for drawing
        self.scene = Scene()  # Initialize the scene
        self.setup_scene()

    def setup_scene(self):
        self.scene.add_system(PhysicsSystem())
        self.scene.add_system(AgeSystem())

    def on_draw(self):
        self.clear()
        self.batch.draw()  # Draw everything in the batch

    def update(self, dt):
        self.scene.update(dt)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            bullet = self.create_bullet(x, y, 10, 50.0, self.batch)
            self.scene.add_entity(bullet)
            
    def create_bullet(self, x, y, radius, speed, batch):
        bullet = Entity()
        bullet.add_component(ShapeComponent.circle(x, y, radius, mass=1.0, batch=batch))
        bullet.add_component(VelocityComponent(speed * cos(random.uniform(0, 2*pi)), speed * sin(random.uniform(0, 2*pi))))
        bullet.add_component(AccelerationComponent())
        bullet.add_component(AgeComponent(2.0))
        return bullet