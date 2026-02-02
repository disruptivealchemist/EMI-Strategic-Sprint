class Mapper:
    def __init__(self):
        self.digital_footprint_map = {}

    def create_map(self, extracted_data):
        for data in extracted_data:
            user_id = data.get('user_id')
            if user_id not in self.digital_footprint_map:
                self.digital_footprint_map[user_id] = {
                    'activities': [],
                    'profiles': []
                }
            self.digital_footprint_map[user_id]['activities'].append(data.get('activity'))
            self.digital_footprint_map[user_id]['profiles'].append(data.get('profile'))

    def get_map(self):
        return self.digital_footprint_map