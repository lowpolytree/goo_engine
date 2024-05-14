import pyglet
from pyglet.shapes import Circle
from pyglet.shapes import Rectangle

class Component:
    pass

class ShapeComponent(Component):
    def __init__(self):
        # Initially, no specific shape is defined
        self.shape = None

    @classmethod
    def circle(cls, x, y, radius, mass=1.0, batch=None):
        obj = cls()
        #position is at 0.0 by default, for rendering and physics position component will be used
        obj.shape = Circle(x, y, radius, batch=batch)
        obj.inverseMass = 1.0 / mass
        return obj
    
    @classmethod
    def rectangle(cls, x, y, width, height, mass=1.0, batch=None):
        obj = cls()
        #position is at 0.0 by default, for rendering and physics position component will be used
        obj.shape = Rectangle(x, y, width, height, batch=batch) 
        obj.width = width
        obj.height = height
        obj.inverseMass = 1.0 / mass
        return obj

    def update_position(self, dx, dy):
        # Update the shape's position by a delta
        if self.shape:
            self.shape.x += dx
            self.shape.y += dy

class VelocityComponent(Component):
    def __init__(self, vx=0, vy=0, damping=1.0):
        self.vx = vx
        self.vy = vy
        self.damping = damping  # Damping factor

class MassComponent(Component):
    def __init__(self, mass=1.0):
        self.mass = mass
        self.inverse_mass = 1.0/self.mass if mass != 0 else float('inf')

class AccelerationComponent(Component):
    
    def __init__(self, ax=0, ay=0):
        self.ax = ax  # Acceleration in the x direction
        self.ay = ay  # Acceleration in the y direction
        self.force_x = 0  # Total force currently applied in the x direction
        self.force_y = 0  # Total force currently applied in the y direction
        self.inverse_mass = 1.0  # Default inverse mass; update as necessary

    def apply_force(self, fx, fy):
        """ Apply an external force to the component. """
        self.force_x += fx
        self.force_y += fy

    def update_acceleration(self):
        """ Update acceleration based on the current total force and inverse mass. """
        self.ax = self.force_x * self.inverse_mass
        self.ay = self.force_y * self.inverse_mass
        #print(f"ax: {self.ax}, ay: {self.ay}")

    def clear_forces(self):
        """ Clear all forces after updating acceleration to prepare for the next frame. """
        self.force_x = 0
        self.force_y = 0

class AgeComponent(Component):
    def __init__(self, age):
        self.age = age
        self.remaining_time = age

class ForceComponent(Component):
    def __init__(self):
        self.forces = []

    def add_force(self, fx, fy):
        self.forces.append((fx, fy))

    def total_force(self):
        total_fx = sum(fx for fx, _ in self.forces)
        total_fy = sum(fy for _, fy in self.forces)
        return total_fx, total_fy
    
    def reset_forces(self):
        self.forces = []