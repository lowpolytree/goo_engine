from components.components import ShapeComponent, VelocityComponent, AgeComponent, MassComponent, ForceComponent
from systems.force_generator import *

class System:
    def update(self, entities, dt):
        raise NotImplementedError


class PhysicsSystem(System):
    def __init__(self):
        self.force_generators = []

    def add_force_generator(self, fg):
        self.force_generators.append(fg)

    def update(self, entities, dt):
        if not entities:  # Early exit if no entities to process
            return
        for entity in entities:
            for generator in self.force_generators:
                generator.apply_force(entity)

            forces = entity.get_component(ForceComponent)
            mass = entity.get_component(MassComponent)
            velocity = entity.get_component(VelocityComponent)
            shape = entity.get_component(ShapeComponent)

            if forces and velocity and mass and shape:
                # Calculate net force
                total_fx, total_fy = forces.total_force()

                #Calculate acceleration
                ax_old = total_fx * mass.inverse_mass
                ay_old = total_fy * mass.inverse_mass

                # Update position
                posx = velocity.vx * dt + 0.5 * ax_old * dt * dt
                posy = velocity.vy * dt + 0.5 * ay_old * dt * dt
                shape.update_position(posx, posy)

                # Update forces for the new position
                for generator in self.force_generators:
                    generator.apply_force(entity)
                total_fx_new, total_fy_new = forces.total_force()

                # Update acceleration
                ax_new = total_fx_new * mass.inverse_mass
                ay_new = total_fy_new * mass.inverse_mass

                # Update velocity
                velocity.vx += 0.5 * (ax_old + ax_new) * dt
                velocity.vy += 0.5 * (ay_old + ay_new) * dt

                # Apply damping to velocity
                velocity.vx *= velocity.damping
                velocity.vy *= velocity.damping

                # Clear forces for the next update cycle
                forces.reset_forces()

class AgeSystem(System):
    def update(self, entities, dt):
        if not entities:  # Early exit if no entities to process
            return
        for entity in entities:
            age = entity.get_component(AgeComponent)
            if age:
                age.remaining_time -= dt
                if age.remaining_time <= 0.0:
                    entity.is_active = False

