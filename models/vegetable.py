from . import db, Item
# from .item import Item

class Vegetable(Item):
    """! The class representing a Vegetable object."""
    __tablename__ = 'vegetable'

    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    premadebox_id = db.Column(db.Integer, db.ForeignKey('premadebox.id'), nullable=True)
    # Relationship with premade boxes
    premadebox = db.relationship('PremadeBox', back_populates='vegetables', foreign_keys=[premadebox_id])

    __mapper_args__ = {
        'polymorphic_identity': 'vegetable',
    }

    def __str__(self) -> str:
        """! The string representation of the Vegetable object.
        
        @return The Vegetable object as a string.
        """
        return f"Vegetable: {self.name}"
    
        
    # @property
    # def name(self) -> str:
    #     """! Method to get the vegetable name.

    #     @return The name of the vegetable as an string.
    #     """
    #     return self._name

    # @name.setter
    # def name(self, new_name: str) -> None:
    #     """! Method to set new name for the vegetable.

    #     @param new_name The new name to set.
    #     """
    #     self._name = new_name

    # @property
    # def premadebox_id(self) -> int:
    #     """! Method to get the premadebox id.

    #     @return The premadebox id as an integer.
    #     """
    #     return self._premadebox_id

#     @property
#     def category(self) -> str:
#         """! Method to get the category of the vegetable.

#         @return The category as a string.
#         """
#         pass

#     @category.setter
#     def category(self, new_category: str) -> None:
#         """! Method to set new category for the vegetable.
        
#         @param new_category The new category to set.
#         """
#         pass


# # VEGGIES_KG = [
#         {'name': 'Carrots', 'price': 1.99, 'available': True},
#         {'name': 'Tomatoes', 'price': 4.99, 'available': True},
#         {'name': 'Onions', 'price': 0.99, 'available': True},
#         {'name': 'Gingers', 'price': 9.99, 'available': True},
#         {'name': 'Garlics', 'price': 41.99, 'available': True},
#         {'name': 'Kumaras', 'price': 5.99, 'available': True},
#         {'name': 'Potatoes', 'price': 1.89, 'available': True}
#     ]
    
#     VEGGIES_PACK = [
#         {'name': 'Carrots (1.5kg)', 'price': 2.89, 'available': True},
#         {'name': 'Cherry Tomatoes (250g)', 'price': 4.99, 'available': True},
#         {'name': 'Baby Spinach (130g)', 'price': 3.99, 'available': True},
#         {'name': 'Washed Lettuce (250g)', 'price': 5.99, 'available': True},
#         {'name': 'Shredded Cabbage (200g)', 'price': 3.99, 'available': True},
#         {'name': 'Beetroots (1kg)', 'price': 2.99, 'available': False},
#         {'name': 'Red Potatoes (5kg)', 'price': 10.99, 'available': True},
#         {'name': 'Rosemary (50g)', 'price': 10.99, 'available': True}
#     ]
    
#     VEGGIES_EACH = [
#         {'name': 'Cabbage', 'price': 2.89, 'available': True},
#         {'name': 'Brocolli', 'price': 1.99, 'available': True},
#         {'name': 'Cauliflower', 'price': 3.99, 'available': True},
#         {'name': 'Pumpkin', 'price': 5.99, 'available': True},
#         {'name': 'Cucumber', 'price': 3.99, 'available': True},
#         {'name': 'Capsicum', 'price': 2.99, 'available': True},
#         {'name': 'Zucchini', 'price': 10.99, 'available': True},
#         {'name': 'Eggplant', 'price': 10.99, 'available': True}
#     ]


    # @classmethod
    # def get_all_vegetables(cls, sort_by: str = 'name') -> list:
    #     """! Class method to retrieve all vegetables from the database.
        
    #     @return A list of all Vegetable instances.
    #     """
    #     try:
    #         all_veggies = []

    #         # Add unit to each vegetable and combine all lists
    #         all_veggies += [{'name': veg['name'], 'price': veg['price'], 'available': veg['available'], 'unit': 'kg'} for veg in cls.VEGGIES_KG]
    #         all_veggies += [{'name': veg['name'], 'price': veg['price'], 'available': veg['available'], 'unit': 'pack'} for veg in cls.VEGGIES_PACK]
    #         all_veggies += [{'name': veg['name'], 'price': veg['price'], 'available': veg['available'], 'unit': 'each'} for veg in cls.VEGGIES_EACH]
    #         return sorted(all_veggies, key=lambda x: x[sort_by])
    #     except Exception as e:
    #         raise ValueError(f"Error retriving all vegetables: {str(e)}")
    
    # @classmethod
    # def get_available_vegetables(cls, sort_by: str = 'name') -> list:
    #     """! Class method to retrieve all available vegetables from the database.
        
    #     @return A list of all available Vegetable instances.
    #     """
    #     try:
    #         all_veggies = cls.get_all_vegetables(sort_by)
    #         return [veg for veg in all_veggies if veg['available']]
    #     except Exception as e:
    #         raise ValueError(f"Error retriving all available vegetables: {str(e)}")