class BrandEntity:
    def __init__(self, name, variations=None):
        self.name = name
        self.variations = variations if variations is not None else []

    def add_variation(self, variation):
        if variation not in self.variations:
            self.variations.append(variation)

    def __repr__(self):
        return f"BrandEntity(name={self.name}, variations={self.variations})"

    def to_dict(self):
        return {
            "name": self.name,
            "variations": self.variations
        }