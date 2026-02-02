import argparse
from digital_footprint.crawler import Crawler
from digital_footprint.mapper import Mapper

def main():
    parser = argparse.ArgumentParser(description="Crawl and generate a digital footprint map.")
    parser.add_argument('--url', type=str, required=True, help='The URL to start crawling from.')
    parser.add_argument('--output', type=str, default='output_map.json', help='The output file for the digital footprint map.')

    args = parser.parse_args()

    # Initialize the Crawler
    crawler = Crawler()
    crawler.start_crawl(args.url)

    # Retrieve the results
    data = crawler.get_results()

    # Initialize the Mapper
    mapper = Mapper()
    footprint_map = mapper.create_map(data)

    # Save the footprint map to the specified output file
    with open(args.output, 'w') as f:
        f.write(footprint_map)

if __name__ == "__main__":
    main()