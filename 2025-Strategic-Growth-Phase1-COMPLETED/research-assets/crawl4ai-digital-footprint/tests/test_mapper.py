import unittest
from digital_footprint.mapper import Mapper

class TestMapper(unittest.TestCase):

    def setUp(self):
        self.mapper = Mapper()

    def test_create_map(self):
        # Sample extracted data for testing
        extracted_data = [
            {"url": "http://example.com", "title": "Example"},
            {"url": "http://test.com", "title": "Test"}
        ]
        expected_output = {
            "Example": "http://example.com",
            "Test": "http://test.com"
        }
        result = self.mapper.create_map(extracted_data)
        self.assertEqual(result, expected_output)

    def test_create_map_empty_data(self):
        result = self.mapper.create_map([])
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()