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
        
class AchoredSpringForceGenerator(ForceGenerator):
    def __init__(self, spring, anchor_pos, spring_coefficient, rest_length):
        self.spring = spring
        self.anchor = anchor_pos
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

class DoubleSpringForceGenerator(ForceGenerator):
    def __init__(self, start_point, end_point, spring_coefficient, rest_length):
        self.start_point = start_point
        self.end_point = end_point
        self.k = spring_coefficient 
        self.rest_length = rest_length
        
    def apply_force(self, entity):
        start_force_comp = self.start_point.get_component(ForceComponent)
        end_force_comp = self.end_point.get_component(ForceComponent)
        start_shape = self.start_point.get_component(ShapeComponent)
        end_shape = self.end_point.get_component(ShapeComponent)
        
        if start_force_comp and end_force_comp and start_shape and end_shape: 
            start_pos = Vec2(start_shape.shape.x, start_shape.shape.y)
            end_pos = Vec2(end_shape.shape.x, end_shape.shape.y)

            displacement = end_pos - start_pos
            distance = displacement.mag
            n_displacement = displacement.normalize() if distance != 0 else Vec2(0, 0)
            
            change_in_length = self.rest_length - distance

            force_x = -self.k * change_in_length * n_displacement.x
            force_y = -self.k * change_in_length * n_displacement.y

            # print(f"Displacement: {displacement}, Distance: {distance}, Change in length: {change_in_length}, Force: {(force_x, force_y)}")

            start_force_comp.add_force(force_x, force_y)
            end_force_comp.add_force(-force_x, -force_y)
