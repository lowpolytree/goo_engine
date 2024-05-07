
class Scene:
    def __init__(self):
        self.entities = []
        self.systems = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_system(self, system):
        self.systems.append(system)

    def update(self, dt):
        for system in self.systems:
            system.update(self.entities, dt)
        self.clean_up()
        print(f"Active Entities: {len(self.entities)}")

    def clean_up(self):
        self.entities = [entity for entity in self.entities if entity.is_active]

    def draw(self):
        for system in self.systems:
            if hasattr(system, 'draw'):
                system.draw(self.entities)