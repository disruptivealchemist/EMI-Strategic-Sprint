import unittest
from src.brand_consolidation.collectors.web_crawler import crawl_web_mentions
from src.brand_consolidation.collectors.social_scraper import scrape_social_mentions
from src.brand_consolidation.collectors.competitor_analyzer import analyze_competitor_mentions

class TestCollectors(unittest.TestCase):

    def test_crawl_web_mentions(self):
        brand_name = "Emery Industries"
        mentions = crawl_web_mentions(brand_name)
        self.assertIsInstance(mentions, list)
        self.assertGreater(len(mentions), 0)

    def test_scrape_social_mentions(self):
        brand_name = "Emery Industries"
        mentions = scrape_social_mentions(brand_name)
        self.assertIsInstance(mentions, list)
        self.assertGreater(len(mentions), 0)

    def test_analyze_competitor_mentions(self):
        competitors = ["Competitor A", "Competitor B"]
        mentions = analyze_competitor_mentions(competitors)
        self.assertIsInstance(mentions, dict)
        self.assertGreater(len(mentions), 0)

if __name__ == '__main__':
    unittest.main()