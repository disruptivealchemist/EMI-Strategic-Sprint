from brand_consolidation.models.brand_entity import BrandEntity
from brand_consolidation.models.mention import Mention

class Consolidator:
    def __init__(self):
        self.entities = {}

    def add_entity(self, brand_name, mention):
        if brand_name not in self.entities:
            self.entities[brand_name] = BrandEntity(name=brand_name)
        self.entities[brand_name].add_mention(mention)

    def consolidate(self):
        consolidated_entities = []
        for entity in self.entities.values():
            consolidated_entities.append(entity)
        return consolidated_entities

    def merge_entities(self, entity1, entity2):
        # Logic to merge two entities
        merged_entity = BrandEntity(name=entity1.name)
        merged_entity.mentions = entity1.mentions + entity2.mentions
        return merged_entity

    def run_consolidation(self):
        # Placeholder for the consolidation logic
        # This could involve more complex logic based on similarity, etc.
        return self.consolidate()