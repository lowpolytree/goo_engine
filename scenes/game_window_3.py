from pyglet.window import key
import random
from math import cos, sin, pi
from entity import Entity
from scenes.scene_base import Scene
from components.components import *
from systems.systems import *

#spawns fireworks

class GameWindow3(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 600)
        self.batch = pyglet.graphics.Batch()  # Create a batch for drawing
        self.scene = Scene()  # Initialize the scene
        self.setup_scene()

    def setup_scene(self):
        self.scene.add_system(PhysicsSystem())
        self.scene.add_system(AgeSystem())
        self.scene.add_system(GravitySystem(-85.0))

    def on_draw(self):

        #change color of particles based on their age
        for entity in self.scene.entities:
            self.change_particle_color(entity)

        self.clear()
        self.batch.draw()  # Draw everything in the batch

    def update(self, dt):
        self.scene.update(dt)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.create_fireworks(x, y, 100, self.batch)

    def create_fireworks(self, x, y, number_of_particles, batch):
        for i in range(number_of_particles):
            # Stagger the creation by adding a small delay for each particle
            delay = i * 0.01  # Delay each particle by 0.01 seconds
            pyglet.clock.schedule_once(self.create_particle, delay, x, y, batch)

    def create_particle(self, dt, x, y, batch):
        random_speed = random.uniform(250.0, 280.0)
        random_radius = random.uniform(2, 2.5)
        epsilon = 0.2
        random_angle = random.uniform(pi/2 - epsilon, pi/2 + epsilon)
        random_age = random.uniform(3.0, 5.0)
        
        p = Entity()
        p.add_component(ShapeComponent.circle(x, y, random_radius, 1.0, batch))
        p.add_component(VelocityComponent(random_speed * cos(random_angle), random_speed * sin(random_angle)))
        p.add_component(AccelerationComponent())
        p.add_component(AgeComponent(random_age))
        self.scene.add_entity(p)
    
    def change_particle_color(self, p):
        sc = p.get_component(ShapeComponent)
        ac = p.get_component(AgeComponent)

        t = ac.remaining_time / ac.age
        start_color = (255, 0, 0)  # Bright yellow
        end_color = (255, 255, 0)  # Black or transparent

        new_color = (
            int(start_color[0] * (1 - t) + end_color[0] * t),
            int(start_color[1] * (1 - t) + end_color[1] * t),
            int(start_color[2] * (1 - t) + end_color[2] * t)
        )

        sc.shape.color = new_color

