# filepath: brand-entity-consolidation/src/scripts/run_consolidation.py

import sys
from brand_consolidation.collectors.web_crawler import crawl_web_mentions
from brand_consolidation.collectors.social_scraper import scrape_social_media_mentions
from brand_consolidation.collectors.competitor_analyzer import analyze_competitors
from brand_consolidation.extractors.mention_extractor import extract_mentions
from brand_consolidation.extractors.entity_extractor import extract_entities
from brand_consolidation.extractors.variation_detector import detect_variations
from brand_consolidation.reconciliation.entity_matcher import match_entities
from brand_consolidation.reconciliation.consolidator import consolidate_entities
from brand_consolidation.utils.config import load_config

def main():
    config = load_config()

    # Step 1: Collect data
    web_mentions = crawl_web_mentions(config['brand_name'])
    social_mentions = scrape_social_media_mentions(config['brand_name'])
    competitor_data = analyze_competitors(config['competitors'])

    # Step 2: Extract mentions and entities
    all_mentions = extract_mentions(web_mentions, social_mentions)
    entities = extract_entities(all_mentions)

    # Step 3: Detect variations
    variations = detect_variations(entities)

    # Step 4: Match entities
    matched_entities = match_entities(variations)

    # Step 5: Consolidate entities
    consolidated_data = consolidate_entities(matched_entities)

    # Output results
    print("Consolidated Brand Entity Data:")
    for entity in consolidated_data:
        print(entity)

if __name__ == "__main__":
    main()