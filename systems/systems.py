from components.components import ShapeComponent, VelocityComponent, AccelerationComponent, AgeComponent

class System:
    def update(self, entities, dt):
        raise NotImplementedError

class PhysicsSystem(System):
    def update(self, entities, dt):
        if not entities:  # Early exit if no entities to process
            return
        for entity in entities:
            acceleration = entity.get_component(AccelerationComponent)
            velocity = entity.get_component(VelocityComponent)
            shape = entity.get_component(ShapeComponent)

            if acceleration and velocity:
                # Update acceleration based on the applied forces
                acceleration.update_acceleration()

                # Update velocity based on acceleration
                velocity.vx += acceleration.ax * dt
                velocity.vy += acceleration.ay * dt

                # Clear forces for the next update cycle
                acceleration.clear_forces()

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

