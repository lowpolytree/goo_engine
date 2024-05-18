from pyglet.window import key
import random
from math import cos, sin, pi
from entity import Entity
from scenes.scene_base import Scene
from components.components import *
from systems.systems import *

# showcasing springs

class GameWindow4(pyglet.window.Window):
    def __init__(self):
        super().__init__(1280, 720)

        self.fps_display = pyglet.window.FPSDisplay(self)

        self.batch = pyglet.graphics.Batch()  # Create a batch for drawing
        self.scene = Scene()  # Initialize the scene
        self.setup_scene()

    def setup_scene(self):

        #entities
        spring1_start = (600, 600)
        spring1_end = (600, 300)
        spring1 = self.create_spring(600, 600, 600, 300, 5.0, 1.0, self.batch)

        #systems
        physics_system = PhysicsSystem()
        gravity_generator = GravityForceGenerator(0.0)
        physics_system.add_force_generator(gravity_generator)

        spring_fgen1 = SpringForceGenerator(spring1_start, 50.0, 250.0)
        physics_system.add_force_generator(spring_fgen1)

        self.scene.add_system(physics_system)

        
    def on_draw(self):

        self.clear()
        self.fps_display.draw()
        self.batch.draw()  # Draw everything in the batch

    def update(self, dt):
        self.scene.update(dt)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            pass

    def create_spring(self, x1, y1, x2, y2, radius, width, batch):
        # Entity for the line
        line_entity = Entity()
        line_component = ShapeComponent.line(x1, y1, x2, y2, width, batch)
        line_entity.add_component(line_component)

        # Entity for the start of the line
        start = Entity()
        circle_component1 = ShapeComponent.circle(x1, y1, radius, batch)
        start.add_component(circle_component1)

        # Entity for the end of the line
        end = Entity()
        circle_component2 = ShapeComponent.circle(x2, y2, radius, batch)
        end.add_component(circle_component2)
        end.add_component(ForceComponent())
        end.add_component(MassComponent())
        end.add_component(VelocityComponent(0.0, 0.0, 0.98))

        # Add all entities to the scene
        self.scene.add_entity(line_entity)
        self.scene.add_entity(start)
        self.scene.add_entity(end)

        # Optionally, keep track of these entities together if needed
        return (line_entity, start, end)

    
