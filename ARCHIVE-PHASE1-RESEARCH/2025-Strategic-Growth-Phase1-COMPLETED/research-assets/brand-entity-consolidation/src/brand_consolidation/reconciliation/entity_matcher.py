from typing import List, Dict
from .similarity_calculator import calculate_similarity
from ..models.brand_entity import BrandEntity

class EntityMatcher:
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    def match_entities(self, entities: List[BrandEntity]) -> List[Dict[str, List[BrandEntity]]]:
        matched_entities = []
        processed = set()

        for i, entity in enumerate(entities):
            if entity in processed:
                continue
            
            similar_entities = [entity]
            processed.add(entity)

            for j in range(i + 1, len(entities)):
                if entities[j] in processed:
                    continue
                
                if self.is_similar(entity, entities[j]):
                    similar_entities.append(entities[j])
                    processed.add(entities[j])

            matched_entities.append({
                'base_entity': entity,
                'variations': similar_entities
            })

        return matched_entities

    def is_similar(self, entity1: BrandEntity, entity2: BrandEntity) -> bool:
        return calculate_similarity(entity1.name, entity2.name) >= self.threshold