from components.components import ShapeComponent, VelocityComponent, AccelerationComponent, AgeComponent, MassComponent, ForceComponent
from systems.force_generator import GravityForceGenerator, DragForceGenerator

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
                ax = total_fx * mass.inverse_mass
                ay = total_fy * mass.inverse_mass

                #print(f"ax: {ax}, ay: {ay}")

                # Update velocity based on acceleration
                velocity.vx += ax * dt
                velocity.vy += ay * dt

                # Clear forces for the next update cycle
                forces.reset_forces()

                # Update position if shape component exists
                if shape:
                    shape.update_position(velocity.vx * dt, velocity.vy * dt)

class GravitySystem(System):
    def __init__(self, gravity = -9.8):
        self.gravity = gravity

    def update(self, entities, dt):
        if not entities:  # Early exit if no entities to process
            return
        for entity in entities:
            accel = entity.get_component(AccelerationComponent)
            if accel:
                accel.apply_force(0, self.gravity)


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

