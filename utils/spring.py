from components.components import ShapeComponent, VelocityComponent, MassComponent, ForceComponent
from systems.force_generator import AchoredSpringForceGenerator, DoubleSpringForceGenerator
from entity import Entity
from systems.systems import PhysicsSystem
from scenes.scene_base import Scene

# Spring : base
# Anchored Spring : derived
# TwoEnded Spring: derived

class Spring():
    def __init__(self, spring_coefficient, rest_length, damping, batch):
        self.k = spring_coefficient
        self.rest_length = rest_length
        self.damping = damping
        self.batch = batch
        self.start_entity = None
        self.end_entity = None
        self.line_entity = None

    def create_spring_entities(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def add_to_scene(self, scene, system):
        raise NotImplementedError("This method should be overridden by subclasses")

    def update(self, dt):
        raise NotImplementedError("This method should be overridden by subclasses")

    def update_connection(self):
        raise NotImplementedError("This method should be overridden by subclasses")

class AnchoredSpring(Spring):
    def __init__(self, anchor_point, movable_point, spring_coefficient, rest_length, damping, batch):
        super().__init__(spring_coefficient, rest_length, damping, batch)
        self.anchor_point = anchor_point
        self.movable_point = movable_point
        self.create_spring_entities()

    def create_spring_entities(self):
        # Implement entity creation for anchored spring
        self.line_entity = Entity()
        self.line_entity.add_component(ShapeComponent.line(*self.anchor_point, *self.movable_point, 1.0, self.batch))

        self.end_entity = Entity()
        self.end_entity.add_component(ShapeComponent.circle(*self.movable_point, 10.0, self.batch))
        self.end_entity.add_component(ForceComponent())
        self.end_entity.add_component(MassComponent(1.0))
        self.end_entity.add_component(VelocityComponent(0.0, 0.0, self.damping))

        self.force_generator = AchoredSpringForceGenerator(self.end_entity, self.anchor_point, self.k, self.rest_length)

    def add_to_scene(self, scene, system):
        scene.add_entity(self.line_entity)
        scene.add_entity(self.end_entity)
        system.add_force_generator(self.force_generator)

    def update_connection(self):
        if self.line_entity and self.end_entity:
            shape = self.line_entity.get_component(ShapeComponent)
            end_pos = self.end_entity.get_component(ShapeComponent).shape.position
            shape.shape.x2, shape.shape.y2 = end_pos

    def update(self, dt):
        self.update_connection()

class DoubleSpring(Spring):
    def __init__(self, start_point, end_point, spring_coefficient, rest_length, damping, batch):
        super().__init__(spring_coefficient, rest_length, damping, batch)
        self.start_point = start_point
        self.end_point = end_point
        self.create_spring_entities()

    def create_spring_entities(self):
        # Entity for the connecting line
        self.line_entity = Entity()
        self.line_entity.add_component(ShapeComponent.line(*self.start_point, *self.end_point, 1.0, self.batch))

        # Entity for the start of the line
        self.start_entity = Entity()
        self.start_entity.add_component(ShapeComponent.circle(*self.start_point, 5.0, self.batch))
        self.start_entity.add_component(ForceComponent())
        self.start_entity.add_component(MassComponent())
        self.start_entity.add_component(VelocityComponent(0.0, 0.0, self.damping))

        # Entity for the end of the line
        self.end_entity = Entity() 
        self.end_entity.add_component(ShapeComponent.circle(*self.end_point, 5.0, self.batch))
        self.end_entity.add_component(ForceComponent())
        self.end_entity.add_component(MassComponent())
        self.end_entity.add_component(VelocityComponent(0.0, 0.0, self.damping))

        self.force_generator = DoubleSpringForceGenerator(self.start_entity, self.end_entity, self.k, self.rest_length)

    def add_to_scene(self, scene, system):
        scene.add_entity(self.start_entity)
        scene.add_entity(self.line_entity)
        scene.add_entity(self.end_entity)
        system.add_force_generator(self.force_generator)

    def update_connection(self):
        if self.line_entity and self.start_entity and self.end_entity:
            line = self.line_entity.get_component(ShapeComponent)
            start_pos = self.start_entity.get_component(ShapeComponent).shape.position
            end_pos = self.end_entity.get_component(ShapeComponent).shape.position
            line.shape.x, line.shape.y = start_pos
            line.shape.x2, line.shape.y2 = end_pos
        
    def update(self, dt):
        self.update_connection()

class SpringSystem():
    def __init__(self):
        pass
    