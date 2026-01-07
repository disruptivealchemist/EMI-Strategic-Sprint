import unittest
from src.brand_consolidation.extractors.mention_extractor import extract_mentions
from src.brand_consolidation.extractors.entity_extractor import extract_entities
from src.brand_consolidation.extractors.variation_detector import detect_variations

class TestExtractors(unittest.TestCase):

    def setUp(self):
        self.sample_data = [
            "Emery Industries is a leading company.",
            "Emery Ind. provides innovative solutions.",
            "Emery Industries, Inc. has a strong market presence."
        ]

    def test_extract_mentions(self):
        mentions = extract_mentions(self.sample_data)
        expected_mentions = [
            "Emery Industries",
            "Emery Ind.",
            "Emery Industries, Inc."
        ]
        self.assertEqual(mentions, expected_mentions)

    def test_extract_entities(self):
        entities = extract_entities(self.sample_data)
        expected_entities = [
            {"name": "Emery Industries", "type": "brand"},
            {"name": "Emery Ind.", "type": "brand"},
            {"name": "Emery Industries, Inc.", "type": "brand"}
        ]
        self.assertEqual(entities, expected_entities)

    def test_detect_variations(self):
        variations = detect_variations(self.sample_data)
        expected_variations = {
            "Emery Industries": ["Emery Ind.", "Emery Industries, Inc."]
        }
        self.assertEqual(variations, expected_variations)

if __name__ == '__main__':
    unittest.main()