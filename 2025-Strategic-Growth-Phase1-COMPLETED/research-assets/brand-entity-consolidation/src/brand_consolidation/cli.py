# filepath: /brand-entity-consolidation/brand-entity-consolidation/src/brand_consolidation/cli.py

import argparse
from brand_consolidation.collectors.web_crawler import crawl_web_mentions
from brand_consolidation.collectors.social_scraper import scrape_social_mentions
from brand_consolidation.collectors.competitor_analyzer import analyze_competitors
from brand_consolidation.extractors.mention_extractor import extract_mentions
from brand_consolidation.extractors.entity_extractor import extract_entities
from brand_consolidation.extractors.variation_detector import detect_variations
from brand_consolidation.reconciliation.consolidator import consolidate_entities

def main():
    parser = argparse.ArgumentParser(description='Brand Entity Consolidation CLI')
    parser.add_argument('--brand', type=str, required=True, help='The brand name to consolidate')
    parser.add_argument('--output', type=str, default='consolidated_results.json', help='Output file for consolidated results')

    args = parser.parse_args()

    # Step 1: Collect data
    web_mentions = crawl_web_mentions(args.brand)
    social_mentions = scrape_social_mentions(args.brand)
    competitor_data = analyze_competitors(args.brand)

    # Step 2: Extract mentions and entities
    mentions = extract_mentions(web_mentions, social_mentions)
    entities = extract_entities(mentions)

    # Step 3: Detect variations
    variations = detect_variations(entities)

    # Step 4: Consolidate entities
    consolidated_data = consolidate_entities(variations)

    # Step 5: Save results
    with open(args.output, 'w') as f:
        json.dump(consolidated_data, f, indent=4)

    print(f'Consolidation complete. Results saved to {args.output}')

if __name__ == '__main__':
    main()