#!/usr/bin/python3
"""Unit tests for Place class"""
import unittest
from unittest.mock import patch
from io import StringIO
from models.place import Place
from models.base_model import BaseModel
from models.review import Review
from models.amenity import Amenity
from os import getenv


class TestPlace(unittest.TestCase):
    """Test cases for the Place class"""

    def test_place_inheritance(self):
        """Test that Place inherits from BaseModel"""
        new_place = Place()
        self.assertIsInstance(new_place, BaseModel)

    def test_place_attributes(self):
        """Test Place attributes"""
        new_place = Place()
        self.assertTrue(hasattr(new_place, 'city_id'))
        self.assertTrue(hasattr(new_place, 'user_id'))
        self.assertTrue(hasattr(new_place, 'name'))
        self.assertTrue(hasattr(new_place, 'description'))
        self.assertTrue(hasattr(new_place, 'number_rooms'))
        self.assertTrue(hasattr(new_place, 'number_bathrooms'))
        self.assertTrue(hasattr(new_place, 'max_guest'))
        self.assertTrue(hasattr(new_place, 'price_by_night'))
        self.assertTrue(hasattr(new_place, 'latitude'))
        self.assertTrue(hasattr(new_place, 'longitude'))
        self.assertTrue(hasattr(new_place, 'amenities'))
        self.assertTrue(hasattr(new_place, 'reviews'))

    def test_amenities_relationship(self):
        """Test the amenities relationship"""
        new_place = Place()
        self.assertEqual(type(new_place.amenities), list)

    def test_reviews_relationship(self):
        """Test the reviews relationship"""
        new_place = Place()
        self.assertEqual(type(new_place.reviews), list)

    def test_amenities_type(self):
        """Test that amenities is a list of Amenity instances"""
        new_place = Place()
        self.assertTrue(all(
            isinstance(amenity, Amenity) for amenity in new_place.amenities))

    def test_reviews_type(self):
        """Test that reviews is a list of Review instances"""
        new_place = Place()
        self.assertTrue(all(
            isinstance(review, Review) for review in new_place.reviews))

    @patch('sys.stdout', new_callable=StringIO)
    def test_str(self, mock_stdout):
        """Test the __str__ method"""
        new_place = Place()
        expected_output = "[Place] ({}) {}".format(
                new_place.id, new_place.__dict__)
        print(new_place)
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)


if __name__ == '__main__':
    unittest.main()
