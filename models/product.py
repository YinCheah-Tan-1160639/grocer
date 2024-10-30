
class Product:

    def __init__(self):

        # List of all vegetables in the store
        self.veggies_kg = [
            {'name': 'Carrots', 'price': 1.99, 'available': True, 'unit': 'kg'},
            {'name': 'Tomatoes', 'price': 4.99, 'available': True, 'unit': 'kg'},
            {'name': 'Onions', 'price': 0.99, 'available': True, 'unit': 'kg'},
            {'name': 'Gingers', 'price': 9.99, 'available': True, 'unit': 'kg'},
            {'name': 'Garlics', 'price': 41.99, 'available': True, 'unit': 'kg'},
            {'name': 'Kumaras', 'price': 5.99, 'available': True, 'unit': 'kg'},
            {'name': 'Potatoes', 'price': 1.89, 'available': True, 'unit': 'kg'}
        ]
            
        self.veggies_pack = [
            {'name': 'Carrots (1.5kg)', 'price': 2.89, 'available': True, 'unit': 'pack'},
            {'name': 'Cherry Tomatoes (250g)', 'price': 4.99, 'available': True, 'unit': 'pack'},
            {'name': 'Baby Spinach (130g)', 'price': 3.99, 'available': True, 'unit': 'pack'},
            {'name': 'Washed Lettuce (250g)', 'price': 5.99, 'available': True, 'unit': 'pack'},
            {'name': 'Shredded Cabbage (200g)', 'price': 3.99, 'available': True, 'unit': 'pack'},
            {'name': 'Beetroots (1kg)', 'price': 2.99, 'available': False, 'unit': 'pack'},
            {'name': 'Red Potatoes (5kg)', 'price': 8.99, 'available': True, 'unit': 'pack'},
            {'name': 'Rosemary (50g)', 'price': 10.99, 'available': True, 'unit': 'pack'}
        ]

        self.veggies_each = [
            {'name': 'Cabbage', 'price': 2.89, 'available': True, 'unit': 'each'},
            {'name': 'Brocolli', 'price': 1.99, 'available': True, 'unit': 'each'},
            {'name': 'Cauliflower', 'price': 3.99, 'available': True, 'unit': 'each'},
            {'name': 'Pumpkin', 'price': 5.99, 'available': True, 'unit': 'each'},
            {'name': 'Cucumber', 'price': 3.99, 'available': True, 'unit': 'each'},
            {'name': 'Capsicum', 'price': 2.99, 'available': True, 'unit': 'each'},
            {'name': 'Eggplant', 'price': 10.99, 'available': True, 'unit': 'each'}
        ]
    
        # List of premade boxes
        self.premade_boxes = [{
            'size': 'Small',
            'price': 20.00,
            'available': False,
            'contents': [
                {'product': self.veggies_kg[6], 'quantity': 2.0},
                {'product': self.veggies_kg[0], 'quantity': 1.5},
                {'product': self.veggies_pack[1], 'quantity': 1},
                {'product': self.veggies_pack[3], 'quantity': 1},
                {'product': self.veggies_each[2], 'quantity': 1}
            ]}, {
            'size': 'Medium',
            'price': 30.00,
            'available': False,
            'contents': [
                {'product': self.veggies_kg[0], 'quantity': 0.5},
                {'product': self.veggies_kg[1], 'quantity': 1.0},
                {'product': self.veggies_pack[6], 'quantity': 1},
                {'product': self.veggies_pack[3], 'quantity': 1},
                {'product': self.veggies_each[2], 'quantity': 1},
                {'product': self.veggies_each[4], 'quantity': 1},
                {'product': self.veggies_each[5], 'quantity': 1}
            ]}, {
            'size': 'Large',
            'price': 40.00,
            'available': False,
            'contents': [
                {'product': self.veggies_kg[1], 'quantity': 0.5},
                {'product': self.veggies_kg[5], 'quantity': 0.5},
                {'product': self.veggies_kg[3], 'quantity': 0.2},
                {'product': self.veggies_pack[2], 'quantity': 1},
                {'product': self.veggies_pack[1], 'quantity': 1},
                {'product': self.veggies_pack[6], 'quantity': 1},                
                {'product': self.veggies_pack[0], 'quantity': 1},
                {'product': self.veggies_each[1], 'quantity': 1},
                {'product': self.veggies_each[2], 'quantity': 1},
                {'product': self.veggies_each[4], 'quantity': 1},
                {'product': self.veggies_each[5], 'quantity': 1}
        ]}]
        
    def get_all_vegetables(self, sort_by: str = 'name') -> list:
        """! Class method to retrieve all vegetables.
        
        @return A list of all vegetables.
        """
        try:
            all_veggies = []

            # Add unit to each vegetable and combine all lists
            all_veggies += [{'name': veg['name'], 'price': veg['price'], 'available': veg['available'], 'unit': veg['unit']} for veg in self.veggies_kg]
            all_veggies += [{'name': veg['name'], 'price': veg['price'], 'available': veg['available'], 'unit': veg['unit']} for veg in self.veggies_pack]
            all_veggies += [{'name': veg['name'], 'price': veg['price'], 'available': veg['available'], 'unit': veg['unit']} for veg in self.veggies_each]
            return sorted(all_veggies, key=lambda x: x[sort_by])
        except Exception as e:
            raise ValueError(f"Error retriving all vegetables: {str(e)}")
        
    def get_available_vegetables(self, sort_by: str = 'name') -> list:
        """! Class method to retrieve all available vegetables.
        
        @return A list of all available vegetables.
        """
        try:
            all_veggies = self.get_all_vegetables(sort_by)
            return [veg for veg in all_veggies if veg['available']]
        except Exception as e:
            raise ValueError(f"Error retriving all available vegetables: {str(e)}")
        
    def get_all_premade_boxes(self) -> list:
        """! Class method to retrieve all premade boxes.
        
        @return A list of all premade boxes.
        """
        sort_box = {"Small": 1, "Medium": 2, "Large": 3}
        try:
            return sorted(self.premade_boxes, key=lambda box: sort_box[box['size']])
        except Exception as e:
            raise ValueError(f"Error retriving all premade boxes: {str(e)}")

    def get_available_premade_boxes(self) -> list:
        """! Class method to retrieve only available premade boxes.
        
        @return A list of available premade boxes.
        """
        try:
            # Call the existing method to get all premade boxes
            all_boxes = self.get_all_premade_boxes()
            # Filter for available boxes
            return [box for box in all_boxes if box['available']]
        except Exception as e:
            raise ValueError(f"Error retrieving available premade boxes: {str(e)}")