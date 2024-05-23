import random
import pyglet.clock
import utils.tags
from typing import List
from math import cos, sin, pi
from components.components import ShapeComponent, VelocityComponent, MassComponent, ForceComponent, AgeComponent
from entity import Entity
from systems.systems import PhysicsSystem, AgeSystem
from scenes.scene_base import Scene

# Particle and ParticleSystem will have some hardcoded values for now, at least until UI is properly implemented

class Particle():
    def __init__(self, batch, radius, pos, velocity, age=5.0, mass=1.0, damping = 1.0):
        self.batch = batch
        self.radius = radius
        self.pos = pos
        self.velocity = velocity
        self.age = age
        self.mass = mass
        self.damping = damping
        self.particle_entity = None

        self.create_particle()

    def create_particle(self):
        self.particle_entity = Entity()
        self.particle_entity.add_component(ShapeComponent.circle(*self.pos, self.radius, self.batch))
        self.particle_entity.add_component(ForceComponent())
        self.particle_entity.add_component(MassComponent(self.mass)) 
        self.particle_entity.add_component(VelocityComponent(*self.velocity, self.damping))
        self.particle_entity.add_component(AgeComponent(self.age))

    def add_to_scene(self, scene: Scene):
        scene.add_entity(self.particle_entity)
    
    def remove_from_scene(self, scene: Scene):
        if self.particle_entity in scene.entities:
            scene.remove_entity(self.particle_entity)

    def change_color(self):
        shape_comp = self.particle_entity.get_component(ShapeComponent)
        age_comp = self.particle_entity.get_component(AgeComponent)

        if shape_comp and age_comp:
            t = age_comp.remaining_time / age_comp.age
            start_color = (255, 0, 0) 
            end_color = (255, 255, 0)  

            new_color = (
                int(start_color[0] * (1 - t) + end_color[0] * t),
                int(start_color[1] * (1 - t) + end_color[1] * t),
                int(start_color[2] * (1 - t) + end_color[2] * t)
            )

            shape_comp.shape.color = new_color
        

class ParticleSystem():
    def __init__(self, batch, scene: Scene):
        self.batch = batch
        self.scene = scene
        self.particles: List[Particle] = []
        self.ageSystem = None

        self.set_up()
    
    def update(self, dt):
        #print("Current number of particles:", len(self.particles))
        self.clean_up()

    def set_up(self):
        self.ageSystem = AgeSystem()
        self.scene.add_system(self.ageSystem)

    def add_particle(self, dt, pos):
        random_speed = random.uniform(250.0, 280.0)
        random_radius = random.uniform(2, 2.5)
        epsilon = 0.2
        random_angle = random.uniform(pi/2 - epsilon, pi/2 + epsilon)
        random_age = random.uniform(3.0, 5.0)
        random_velocity = (random_speed * cos(random_angle), random_speed * sin(random_angle))

        p = Particle(self.batch, random_radius, pos, random_velocity, random_age)
        self.particles.append(p)
        p.add_to_scene(self.scene)

    def create_firework(self, origin, number_of_particles):
        for i in range(number_of_particles):
            delay = i * 0.005  # Delay each particle by 0.005 seconds
            pyglet.clock.schedule_once(self.add_particle, delay, origin)    
    
    def draw(self):
        if self.particles:
            for p in self.particles:
                p.change_color()

    def clean_up(self):
        inactive_particles = [p for p in self.particles if not p.particle_entity.is_active]
        for p in inactive_particles:
            p.remove_from_scene(self.scene)
            self.particles = [p for p in self.particles if p.particle_entity.is_active]