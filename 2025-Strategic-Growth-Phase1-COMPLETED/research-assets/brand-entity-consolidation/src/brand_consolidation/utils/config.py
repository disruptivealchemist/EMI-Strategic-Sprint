# Configuration settings for the brand entity consolidation project

# Define the base URL for web crawling
BASE_URL = "https://example.com"

# Specify the social media platforms to scrape
SOCIAL_MEDIA_PLATFORMS = [
    "twitter",
    "facebook",
    "instagram"
]

# Set the maximum number of mentions to collect
MAX_MENTIONS = 1000

# Define the output file for consolidated data
OUTPUT_FILE = "consolidated_brand_data.json"

# Set the logging level
LOGGING_LEVEL = "INFO"

# Define the similarity threshold for entity matching
SIMILARITY_THRESHOLD = 0.85

# Specify the path to the settings YAML file
SETTINGS_FILE = "../config/settings.yaml"