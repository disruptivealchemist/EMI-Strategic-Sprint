import unittest
from src.brand_consolidation.reconciliation.entity_matcher import EntityMatcher
from src.brand_consolidation.models.brand_entity import BrandEntity

class TestEntityMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = EntityMatcher()
        self.entity1 = BrandEntity(name="Emery Industries", variations=["Emery Ind.", "Emery Inc."])
        self.entity2 = BrandEntity(name="Emery Industries", variations=["Emery Industries LLC", "Emery Industries"])
        self.entity3 = BrandEntity(name="Emery", variations=["Emery Corp.", "Emery Co."])

    def test_match_identical_entities(self):
        result = self.matcher.match(self.entity1, self.entity2)
        self.assertTrue(result)

    def test_match_different_entities(self):
        result = self.matcher.match(self.entity1, self.entity3)
        self.assertFalse(result)

    def test_match_with_variations(self):
        self.entity1.variations.append("Emery Industries LLC")
        result = self.matcher.match(self.entity1, self.entity2)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()