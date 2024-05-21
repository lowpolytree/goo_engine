from components.components import ShapeComponent, VelocityComponent, MassComponent, ForceComponent
from pyglet.math import Vec2

class ForceGenerator:
    def apply_force(self, entity):
        raise NotImplementedError("Each force generator must implement this!")
    
class GravityForceGenerator(ForceGenerator):
    def __init__(self, gravity=-9.8):
        self.gravity = gravity

    def apply_force(self, entity):
        mass = entity.get_component(MassComponent)
        if mass:
            force = mass.mass * self.gravity
            entity.get_component(ForceComponent).add_force(0, force)

class DragForceGenerator(ForceGenerator):
    def __init__(self, k):
        self.k = k # Drag constant, adjust based on your simulation needs 

    def apply_force(self, entity):
        velocity = entity.get_component(VelocityComponent)
        if velocity:
            drag_fx = -self.k * velocity.vx
            drag_fy = -self.k * velocity.vy
            
            entity.get_component(ForceComponent).add_force(drag_fx, drag_fy)
        
class SpringForceGenerator(ForceGenerator):
    def __init__(self, spring, anchor, spring_coefficient, rest_length):
        self.spring = spring
        self.anchor = anchor
        self.k = spring_coefficient 
        self.rest_length = rest_length
        
    def apply_force(self, entity):
        force_comp = self.spring.get_component(ForceComponent)
        shape = self.spring.get_component(ShapeComponent)
        
        if shape and force_comp: 
            end_point = Vec2(shape.shape.x, shape.shape.y)
            fixed_point = Vec2(self.anchor[0], self.anchor[1])

            displacement = fixed_point - end_point
            distance = displacement.mag
            n_displacement = displacement.normalize() if distance != 0 else Vec2(0, 0)
            
            change_in_length = self.rest_length - distance

            force_x = -self.k * change_in_length * n_displacement.x
            force_y = -self.k * change_in_length * n_displacement.y

            #print(f"Displacement: {displacement}, Distance: {distance}, Change in length: {change_in_length}, Force: {(force_x, force_y)}")

            force_comp.add_force(force_x, force_y)
