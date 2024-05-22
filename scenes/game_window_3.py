from pyglet.window import key
import random
from math import cos, sin, pi
from entity import Entity
from scenes.scene_base import Scene
from components.components import *
from systems.systems import *
from utils.particle import ParticleSystem

#spawns fireworks with ParticleSystem

class GameWindow3(pyglet.window.Window):
    def __init__(self):
        super().__init__(1280, 720)

        self.fps_display = pyglet.window.FPSDisplay(self)
        self.physics_system = PhysicsSystem()
        self.batch = pyglet.graphics.Batch() 
        self.scene = Scene()  
        self.particle_system = None

        self.setup_scene()

    def setup_scene(self):
        gravity_generator = GravityForceGenerator(-85.0)
        drag_generator = DragForceGenerator(0.1)
        self.physics_system.add_force_generator(gravity_generator)
        self.physics_system.add_force_generator(drag_generator)

        self.scene.add_system(self.physics_system)

        self.particle_system = ParticleSystem(self.batch, self.scene)
        self.particle_system.create_firework((300, 200), 100)

    def on_draw(self):
        if self.particle_system:
            self.particle_system.draw()

        self.clear()
        self.fps_display.draw()
        self.batch.draw() 

    def update(self, dt):
        self.scene.update(dt)
        if self.particle_system:
            self.particle_system.update(dt)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            pass


