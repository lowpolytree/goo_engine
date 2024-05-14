from components.components import ShapeComponent, VelocityComponent, AccelerationComponent, AgeComponent, MassComponent, ForceComponent

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
        
