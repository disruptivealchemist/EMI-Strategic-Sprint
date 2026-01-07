# Example usage of the Crawl4AI Digital Footprint project

from digital_footprint.crawler import Crawler
from digital_footprint.extractor import Extractor
from digital_footprint.mapper import Mapper

def main():
    # Initialize the Crawler
    crawler = Crawler()
    
    # Start the crawling process
    crawler.start_crawl("https://example.com")
    
    # Retrieve the results
    crawled_data = crawler.get_results()
    
    # Initialize the Extractor
    extractor = Extractor()
    
    # Extract relevant data from the crawled data
    extracted_data = extractor.extract_data(crawled_data)
    
    # Initialize the Mapper
    mapper = Mapper()
    
    # Create a digital footprint map based on the extracted data
    digital_map = mapper.create_map(extracted_data)
    
    # Print the digital footprint map
    print(digital_map)

if __name__ == "__main__":
    main()