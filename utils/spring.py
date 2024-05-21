from components.components import ShapeComponent, VelocityComponent, MassComponent, ForceComponent
from systems.force_generator import SpringForceGenerator
from entity import Entity
from systems.systems import PhysicsSystem
from scenes.scene_base import Scene

class Spring():
    def __init__(self, start_point, end_point, spring_coefficient, rest_length, batch):
        self.start_point = start_point
        self.end_point = end_point
        self.k = spring_coefficient
        self.rest_length = rest_length
        self.batch = batch
        self.force_generator = None
        self.line_entity = None
        self.start_entity = None
        self.end_entity = None

        self.create_spring_entities()
        
    def create_spring_entities(self):

        # Entity for the connecting line
        self.line_entity = Entity()
        self.line_entity.add_component(ShapeComponent.line(*self.start_point, *self.end_point, 1.0, self.batch))

        # Entity for the start of the line
        self.start_entity = Entity()
        self.start_entity.add_component(ShapeComponent.circle(*self.start_point, 5.0, self.batch))

        # Entity for the end of the line
        self.end_entity = Entity()
        self.end_entity.add_component(ShapeComponent.circle(*self.end_point, 5.0, self.batch))
        self.end_entity.add_component(ForceComponent())
        self.end_entity.add_component(MassComponent())
        self.end_entity.add_component(VelocityComponent(0.0, 0.0, 0.98))

        self.force_generator = SpringForceGenerator(self.end_entity, self.start_point, self.k, self.rest_length)

    def add_to_scene(self, scene : Scene, system : PhysicsSystem):
        scene.add_entity(self.line_entity)
        scene.add_entity(self.start_entity)
        scene.add_entity(self.end_entity)
        system.add_force_generator(self.force_generator)

    def update(self, dt):
        self.update_connection()

    def update_connection(self):
        if self.line_entity and self.end_entity:
            shape = self.line_entity.get_component(ShapeComponent)
            end_pos = self.end_entity.get_component(ShapeComponent).shape.position
            shape.shape.x2, shape.shape.y2 = end_pos



    