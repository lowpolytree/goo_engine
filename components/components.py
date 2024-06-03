import pyglet
from pyglet.shapes import Circle, Rectangle, Line

class Component:
    pass

class ShapeComponent(Component):
    def __init__(self):
        # Initially, no specific shape is defined
        self.shape = None

    @classmethod
    def line(cls, x1, y1, x2, y2, width, batch=None):
        obj = cls()
        obj.shape = Line(x1, y1, x2, y2, width, batch=batch)
        return obj

    @classmethod
    def circle(cls, x, y, radius, batch=None):
        obj = cls()
        obj.shape = Circle(x, y, radius, batch=batch)
        return obj
    
    @classmethod
    def rectangle(cls, x, y, width, height, batch=None):
        obj = cls()
        obj.shape = Rectangle(x, y, width, height, batch=batch) 
        obj.width = width
        obj.height = height
        return obj

    def update_position(self, dx, dy):
        # Update the shape's position by a delta
        if self.shape:
            self.shape.position = (self.shape.x + dx, self.shape.y + dy)

class VelocityComponent(Component):
    def __init__(self, vx=0, vy=0, damping=1.0):
        self.vx = vx
        self.vy = vy
        self.damping = damping  # Damping factor

class MassComponent(Component):
    def __init__(self, mass=1.0):
        self.mass = mass
        self.inverse_mass = 1.0/self.mass if mass != 0 else float('inf')

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