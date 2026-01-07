from typing import List, Dict
import re

def extract_mentions(text: str, brand_name: str) -> List[str]:
    """
    Extracts brand mentions from the given text.

    Args:
        text (str): The text to search for brand mentions.
        brand_name (str): The brand name to look for.

    Returns:
        List[str]: A list of extracted brand mentions.
    """
    # Create a regex pattern to match variations of the brand name
    pattern = re.compile(r'\b' + re.escape(brand_name) + r'\b', re.IGNORECASE)
    mentions = pattern.findall(text)
    return mentions

def extract_mentions_from_data(data: List[Dict[str, str]], brand_name: str) -> List[str]:
    """
    Extracts brand mentions from a list of data entries.

    Args:
        data (List[Dict[str, str]]): A list of data entries containing text.
        brand_name (str): The brand name to look for.

    Returns:
        List[str]: A list of extracted brand mentions from all entries.
    """
    all_mentions = []
    for entry in data:
        if 'text' in entry:
            mentions = extract_mentions(entry['text'], brand_name)
            all_mentions.extend(mentions)
    return all_mentions