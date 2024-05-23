import utils.tags

class Entity:
    _id_counter = 0

    def __init__(self):
        self.id = Entity._id_counter
        Entity._id_counter += 1
        self.is_active = True
        self.components = {}
        self.tags = set() #to avoid duplicates

    def add_tag(self, tag):
        self.tags.add(tag)
    
    def remove_tag(self, tag):
        self.tags.discard(tag)  # Using discard to avoid KeyError if the tag does not exist

    def has_tag(self, tag):
        return tag in self.tags

    def get_all_tags(self):
        return list(self.tags)

    def add_component(self, component):
        self.components[component.__class__] = component

    def get_component(self, component_type):
        return self.components.get(component_type, None)