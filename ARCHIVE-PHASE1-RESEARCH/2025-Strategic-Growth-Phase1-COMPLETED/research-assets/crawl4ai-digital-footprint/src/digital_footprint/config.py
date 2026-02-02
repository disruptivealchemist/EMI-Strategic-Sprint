# Configuration settings for the digital footprint project

import os

class Config:
    """Configuration settings for the digital footprint project."""
    
    # Default parameters
    DEFAULT_CRAWL_DEPTH = 3
    DEFAULT_TIMEOUT = 10  # seconds
    DEFAULT_USER_AGENT = "Crawl4AI/1.0"
    
    @staticmethod
    def load_env_variables():
        """Load environment variables from a .env file or system environment."""
        from dotenv import load_dotenv
        load_dotenv()

        # Load any additional environment variables here
        Config.CRAWL_DEPTH = int(os.getenv("CRAWL_DEPTH", Config.DEFAULT_CRAWL_DEPTH))
        Config.TIMEOUT = int(os.getenv("TIMEOUT", Config.DEFAULT_TIMEOUT))
        Config.USER_AGENT = os.getenv("USER_AGENT", Config.DEFAULT_USER_AGENT)

# Load configuration settings
Config.load_env_variables()