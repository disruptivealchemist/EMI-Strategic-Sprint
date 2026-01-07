def detect_variations(brand_name, mentions):
    variations = set()
    for mention in mentions:
        if brand_name.lower() in mention.lower():
            variations.add(mention)
    return variations

def standardize_variation(variation):
    # Example standardization logic
    return variation.strip().lower()

def consolidate_variations(brand_name, mentions):
    detected_variations = detect_variations(brand_name, mentions)
    standardized_variations = {standardize_variation(var) for var in detected_variations}
    return standardized_variations

# Example usage
if __name__ == "__main__":
    brand_name = "Emery Industries"
    mentions = [
        "Emery Industries",
        "emery industries",
        "Emery Ind.",
        "Emery Ind",
        "Emery Industries Inc."
    ]
    variations = consolidate_variations(brand_name, mentions)
    print(variations)