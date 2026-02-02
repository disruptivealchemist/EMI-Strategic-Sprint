import requests
import csv
from datetime import datetime
import time
import json
from urllib.parse import quote
import re

class BrandEntityCrawler:
    def __init__(self):
        self.brand_variations = [
            "Emery Industries",
            "Emery Ind", 
            "EMI",
            "Emery Industries Australia",
            "Emery Stainless Steel",
            "emeryindustries.com",
            "emeryindustries.com.au"
        ]
        self.results = []
        
    def search_google(self, query, num_results=10):
        """Search Google for brand mentions (you'd need to implement with Google Custom Search API)"""
        # Placeholder - would use Google Custom Search API
        print(f"Searching Google for: {query}")
        return []
    
    def search_social_platforms(self, brand_name):
        """Search social platforms for brand mentions"""
        platforms = {
            'linkedin': f"https://www.linkedin.com/search/results/companies/?keywords={quote(brand_name)}",
            'facebook': f"https://www.facebook.com/search/pages/?q={quote(brand_name)}",
            'twitter': f"https://twitter.com/search?q={quote(brand_name)}"
        }
        
        mentions = []
        for platform, url in platforms.items():
            mentions.append({
                'platform': platform,
                'search_url': url,
                'brand_variation': brand_name,
                'found_at': datetime.now().isoformat()
            })
        
        return mentions
    
    def crawl_specific_domains(self):
        """Crawl specific domains for brand mentions"""
        domains_to_check = [
            "linkedin.com",
            "facebook.com", 
            "twitter.com",
            "reddit.com",
            "quora.com",
            "industry-specific-sites.com"
        ]
        
        mentions = []
        for domain in domains_to_check:
            for variation in self.brand_variations:
                mention = {
                    'domain': domain,
                    'brand_variation': variation,
                    'search_query': f'site:{domain} "{variation}"',
                    'collected_at': datetime.now().isoformat(),
                    'status': 'pending_search'
                }
                mentions.append(mention)
        
        return mentions
    
    def extract_entity_variations(self, text):
        """Extract potential brand variations from text"""
        patterns = [
            r'Emery\s*Industries?',
            r'EMI\b',
            r'Emery\s*Ind\.?',
            r'emeryindustries\.com\.?a?u?',
            r'Emery\s*Stainless\s*Steel'
        ]
        
        found_variations = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            found_variations.extend(matches)
        
        return list(set(found_variations))
    
    def consolidate_mentions(self):
        """Consolidate and standardize brand mentions"""
        consolidated = {}
        
        for variation in self.brand_variations:
            # Group similar variations
            canonical_name = self.get_canonical_name(variation)
            if canonical_name not in consolidated:
                consolidated[canonical_name] = {
                    'canonical_name': canonical_name,
                    'variations': [],
                    'mentions': [],
                    'platforms': set(),
                    'confidence_score': 0.0
                }
            
            consolidated[canonical_name]['variations'].append(variation)
        
        return consolidated
    
    def get_canonical_name(self, variation):
        """Determine canonical name for brand variation"""
        variation_lower = variation.lower()
        
        if 'emery industries' in variation_lower:
            return 'Emery Industries'
        elif variation_lower == 'emi':
            return 'Emery Industries'
        elif 'emeryindustries.com' in variation_lower:
            return 'Emery Industries'
        else:
            return 'Emery Industries'  # Default canonical name
    
    def run_crawl(self):
        """Run the complete brand entity crawl"""
        print("🔍 Starting Brand Entity Consolidation Crawl...")
        
        # 1. Collect social platform mentions
        print("\n📱 Searching social platforms...")
        for variation in self.brand_variations:
            social_mentions = self.search_social_platforms(variation)
            self.results.extend(social_mentions)
        
        # 2. Crawl specific domains
        print("\n🌐 Crawling specific domains...")
        domain_mentions = self.crawl_specific_domains()
        self.results.extend(domain_mentions)
        
        # 3. Consolidate findings
        print("\n🔧 Consolidating brand entities...")
        consolidated = self.consolidate_mentions()
        
        # 4. Save results
        self.save_results(consolidated)
        
        print(f"\n✅ Crawl complete! Found {len(self.results)} potential mentions.")
        print(f"📊 Consolidated into {len(consolidated)} canonical entities.")
        
        return consolidated
    
    def save_results(self, consolidated_data):
        """Save results to CSV and JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed mentions
        csv_filename = f"brand_entity_mentions_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['platform', 'brand_variation', 'search_url', 'found_at', 'canonical_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.results:
                result['canonical_name'] = self.get_canonical_name(result.get('brand_variation', ''))
                writer.writerow(result)
        
        # Save consolidated summary
        json_filename = f"brand_entity_consolidated_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(consolidated_data, jsonfile, indent=2, default=str)
        
        print(f"💾 Results saved to {csv_filename} and {json_filename}")

def main():
    """Run the brand entity consolidation crawl"""
    crawler = BrandEntityCrawler()
    results = crawler.run_crawl()
    
    # Print summary
    print("\n📋 CONSOLIDATION SUMMARY:")
    print("=" * 50)
    
    for canonical_name, data in results.items():
        print(f"\n🏢 {canonical_name}")
        print(f"   Variations found: {len(data['variations'])}")
        print(f"   Variations: {', '.join(data['variations'])}")
        print(f"   Platforms: {len(data['platforms'])}")

if __name__ == "__main__":
    main()