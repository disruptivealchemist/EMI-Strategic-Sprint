import unittest
from digital_footprint.crawler import Crawler

class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()

    def test_start_crawl(self):
        result = self.crawler.start_crawl("http://example.com")
        self.assertTrue(result)

    def test_get_results(self):
        self.crawler.start_crawl("http://example.com")
        results = self.crawler.get_results()
        self.assertIsInstance(results, list)

    def test_crawl_invalid_url(self):
        with self.assertRaises(ValueError):
            self.crawler.start_crawl("invalid-url")

if __name__ == '__main__':
    unittest.main()