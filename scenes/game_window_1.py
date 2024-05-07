from pyglet.window import key
import random
from entity import Entity
from scenes.scene_base import Scene
from components.components import *
from systems.systems import *

class GameWindow1(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 600)
        self.batch = pyglet.graphics.Batch()  # Create a batch for drawing
        self.scene = Scene()  # Initialize the scene
        self.setup_scene()
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)  # Listen for key presses

    def setup_scene(self):
        # Set up a single entity with initial position and zero velocity
        entity = Entity()
        entity.add_component(ShapeComponent.circle(100, 100, 10, mass=1.0, batch=self.batch))
        entity.add_component(VelocityComponent(0, 0))
        entity.add_component(AccelerationComponent(0, 0))
        self.scene.add_entity(entity)
        self.scene.add_system(PhysicsSystem())

    def on_draw(self):
        self.clear()
        self.batch.draw()  # Draw everything in the batch

    def update(self, dt):
        # Update entity velocities based on key input
        entity = self.scene.entities[0]  # Assuming there's only one entity
        velocity = entity.get_component(VelocityComponent)

        if self.keys[key.LEFT]:
            velocity.vx = -100  # Move left
        elif self.keys[key.RIGHT]:
            velocity.vx = 100   # Move right
        if self.keys[key.UP]:
            velocity.vy = 100   # Move up
        elif self.keys[key.DOWN]:
            velocity.vy = -100  # Move down

        self.scene.update(dt)

    def on_key_release(self, symbol, modifiers):
        # Reset velocities on key release for smooth control
        entity = self.scene.entities[0]
        velocity = entity.get_component(VelocityComponent)
        if symbol in (key.LEFT, key.RIGHT):
            velocity.vx = 0
        if symbol in (key.UP, key.DOWN):
            velocity.vy = 0
