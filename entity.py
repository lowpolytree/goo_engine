class Entity:
    _id_counter = 0

    def __init__(self):
        self.id = Entity._id_counter
        Entity._id_counter += 1
        self.is_active = True
        self.components = {}

    def add_component(self, component):
        self.components[component.__class__] = component

    def get_component(self, component_type):
        return self.components.get(component_type, None)